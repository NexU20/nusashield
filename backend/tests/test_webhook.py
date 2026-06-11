"""Tests for webhook subscription CRUD and severity-filtered dispatch.

Importing WebhookSubscription at module level registers the table on
Base.metadata so the conftest db_engine fixture creates it.
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient

import app.services.webhook as webhook_service
from app.models.webhook import WebhookSubscription
from app.services.webhook import dispatch_webhooks

_KEY = {"X-API-Key": "sharkfin-demo-key-2026"}


# ── Fake httpx client so dispatch never touches the network ──


class _FakeResp:
    status_code = 200


class _FakeClient:
    """Records every POST and returns HTTP 200 without any real request."""

    calls: list[dict] = []

    def __init__(self, *args, **kwargs) -> None:
        pass

    async def __aenter__(self) -> "_FakeClient":
        return self

    async def __aexit__(self, *args) -> bool:
        return False

    async def post(self, url, json=None, headers=None):
        _FakeClient.calls.append({"url": url, "json": json, "headers": headers})
        return _FakeResp()


@pytest.fixture(autouse=True)
def _patch_httpx(monkeypatch):
    _FakeClient.calls = []
    monkeypatch.setattr(webhook_service.httpx, "AsyncClient", _FakeClient)


# ── CRUD endpoints ──


class TestWebhookCRUD:
    @pytest.mark.asyncio
    async def test_register_requires_auth(self, client: AsyncClient):
        resp = await client.post(
            "/api/v1/alerts/webhook/register",
            json={"url": "https://soc.bank.id/hook", "institution": "BRI",
                  "min_severity": "HIGH", "api_key": "subkey"},
        )
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_register_list_delete(self, client: AsyncClient):
        reg = await client.post(
            "/api/v1/alerts/webhook/register",
            headers=_KEY,
            json={"url": "https://soc.bank.id/hook", "institution": "BRI",
                  "min_severity": "HIGH", "api_key": "subkey"},
        )
        assert reg.status_code == 200
        sub_id = reg.json()["subscription_id"]

        listed = await client.get("/api/v1/alerts/webhook/subscriptions", headers=_KEY)
        assert listed.status_code == 200
        assert any(s["id"] == sub_id for s in listed.json())

        deleted = await client.delete(f"/api/v1/alerts/webhook/{sub_id}", headers=_KEY)
        assert deleted.status_code == 200

        # Deactivated subscriptions disappear from the active list.
        listed_after = await client.get(
            "/api/v1/alerts/webhook/subscriptions", headers=_KEY
        )
        assert all(s["id"] != sub_id for s in listed_after.json())


# ── Dispatch logic ──


class TestDispatch:
    @pytest.mark.asyncio
    async def test_no_subscribers_returns_zero(self, db_session):
        sent = await dispatch_webhooks({"threat_id": "x"}, "CRITICAL", db_session)
        assert sent == 0
        assert _FakeClient.calls == []

    @pytest.mark.asyncio
    async def test_severity_filter(self, db_session):
        # HIGH subscriber should get a CRITICAL alert; CRITICAL-only subscriber
        # should NOT get a MEDIUM alert.
        db_session.add_all([
            WebhookSubscription(
                url="https://high.soc/hook", institution="BRI",
                min_severity="HIGH", api_key="k1",
            ),
            WebhookSubscription(
                url="https://critical.soc/hook", institution="BCA",
                min_severity="CRITICAL", api_key="k2",
            ),
        ])
        await db_session.commit()

        sent = await dispatch_webhooks(
            {"threat_id": "abc", "severity": "MEDIUM"}, "MEDIUM", db_session
        )
        # Neither HIGH nor CRITICAL subscriber wants a MEDIUM alert.
        assert sent == 0

        _FakeClient.calls = []
        sent = await dispatch_webhooks(
            {"threat_id": "abc", "severity": "CRITICAL"}, "CRITICAL", db_session
        )
        # Both subscribers want CRITICAL.
        assert sent == 2
        assert {c["url"] for c in _FakeClient.calls} == {
            "https://high.soc/hook", "https://critical.soc/hook"
        }
        # Subscriber key is forwarded, payload is masked-only (no raw content).
        for c in _FakeClient.calls:
            assert c["headers"]["X-SHARK-Fin-Key"] in {"k1", "k2"}
            assert c["json"]["event"] == "threat.detected"

    @pytest.mark.asyncio
    async def test_inactive_subscriber_skipped(self, db_session):
        db_session.add(WebhookSubscription(
            url="https://off.soc/hook", institution="BNI",
            min_severity="LOW", api_key="k3", active=False,
        ))
        await db_session.commit()

        sent = await dispatch_webhooks(
            {"threat_id": "abc"}, "CRITICAL", db_session
        )
        assert sent == 0
