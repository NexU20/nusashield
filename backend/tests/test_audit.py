"""Tests for the audit trail: privileged actions are recorded and queryable."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.models.audit import AuditLog, fingerprint
from app.models.threat import Threat

_KEY = {"X-API-Key": "sharkfin-demo-key-2026"}


def test_fingerprint_is_non_reversible():
    fp = fingerprint("sharkfin-demo-key-2026")
    assert fp.startswith("key:")
    assert "sharkfin-demo-key-2026" not in fp
    assert fingerprint(None) == "anonymous"
    # Deterministic + key-specific.
    assert fp == fingerprint("sharkfin-demo-key-2026")
    assert fp != fingerprint("another-key")


class TestAuditRecording:
    @pytest.mark.asyncio
    async def test_status_update_is_audited(
        self, client: AsyncClient, sample_threat: Threat
    ):
        await client.patch(
            f"/api/v1/threats/{sample_threat.id}/status",
            json={"status": "VERIFIED", "note": "confirmed by analyst"},
            headers=_KEY,
        )
        resp = await client.get("/api/v1/audit?action=threat.status_update", headers=_KEY)
        assert resp.status_code == 200
        entries = resp.json()
        assert len(entries) == 1
        e = entries[0]
        assert e["target_id"] == str(sample_threat.id)
        assert e["detail"]["from"] == "NEW"
        assert e["detail"]["to"] == "VERIFIED"
        assert e["actor"].startswith("key:")

    @pytest.mark.asyncio
    async def test_report_export_is_audited(
        self, client: AsyncClient, sample_threat: Threat
    ):
        await client.get(
            f"/api/v1/threats/{sample_threat.id}/report?format=ojk", headers=_KEY
        )
        resp = await client.get("/api/v1/audit?action=report.export", headers=_KEY)
        entries = resp.json()
        assert len(entries) == 1
        assert entries[0]["detail"]["format"] == "ojk"


class TestWebhookAudit:
    @pytest.mark.asyncio
    async def test_register_and_delete_are_audited(self, client: AsyncClient):
        reg = await client.post(
            "/api/v1/alerts/webhook/register",
            headers=_KEY,
            json={"url": "https://soc.x/h", "institution": "BRI",
                  "min_severity": "HIGH", "api_key": "subkey"},
        )
        sub_id = reg.json()["subscription_id"]
        await client.delete(f"/api/v1/alerts/webhook/{sub_id}", headers=_KEY)

        resp = await client.get("/api/v1/audit", headers=_KEY)
        actions = [e["action"] for e in resp.json()]
        assert "webhook.register" in actions
        assert "webhook.delete" in actions


class TestAuditAuth:
    @pytest.mark.asyncio
    async def test_audit_requires_api_key(self, client: AsyncClient):
        resp = await client.get("/api/v1/audit")
        assert resp.status_code == 401
