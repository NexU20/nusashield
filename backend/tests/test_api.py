"""Integration tests for the threats API.

Uses a real PostgreSQL database (from docker-compose) to verify
endpoint behaviour with actual data. Fixtures are in conftest.py.
"""

from __future__ import annotations

import uuid

import pytest
from httpx import AsyncClient

from app.models.threat import Threat


class TestListThreats:
    @pytest.mark.asyncio
    async def test_empty_list(self, client: AsyncClient):
        resp = await client.get("/api/v1/threats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert "limit" in data
        assert "offset" in data

    @pytest.mark.asyncio
    async def test_with_data(self, client: AsyncClient, sample_threat: Threat):
        resp = await client.get("/api/v1/threats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        item = data["items"][0]
        assert item["id"] == str(sample_threat.id)
        assert item["source_type"] == "TELEGRAM"
        assert item["severity"] == "HIGH"
        assert item["risk_score"] == 65

    @pytest.mark.asyncio
    async def test_filter_by_severity(
        self, client: AsyncClient, sample_threat: Threat
    ):
        resp = await client.get("/api/v1/threats?severity=HIGH")
        assert resp.json()["total"] == 1

        resp = await client.get("/api/v1/threats?severity=LOW")
        assert resp.json()["total"] == 0

    @pytest.mark.asyncio
    async def test_filter_by_source_type(
        self, client: AsyncClient, sample_threat: Threat
    ):
        resp = await client.get("/api/v1/threats?source_type=TELEGRAM")
        assert resp.json()["total"] == 1

        resp = await client.get("/api/v1/threats?source_type=PASTE")
        assert resp.json()["total"] == 0

    @pytest.mark.asyncio
    async def test_filter_by_institution(
        self, client: AsyncClient, sample_threat: Threat
    ):
        resp = await client.get("/api/v1/threats?institution=BRI")
        assert resp.json()["total"] == 1

        resp = await client.get("/api/v1/threats?institution=BCA")
        assert resp.json()["total"] == 0

    @pytest.mark.asyncio
    async def test_pagination(self, client: AsyncClient, sample_threat: Threat):
        resp = await client.get("/api/v1/threats?limit=1&offset=0")
        assert resp.json()["total"] == 1
        assert len(resp.json()["items"]) == 1

        resp = await client.get("/api/v1/threats?limit=1&offset=1")
        assert len(resp.json()["items"]) == 0


class TestGetThreat:
    @pytest.mark.asyncio
    async def test_found(self, client: AsyncClient, sample_threat: Threat):
        resp = await client.get(f"/api/v1/threats/{sample_threat.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == str(sample_threat.id)
        assert "detected_entities" in data
        assert "content_preview" in data

    @pytest.mark.asyncio
    async def test_not_found(self, client: AsyncClient):
        fake_id = uuid.uuid4()
        resp = await client.get(f"/api/v1/threats/{fake_id}")
        assert resp.status_code == 404


class TestUpdateStatus:
    @pytest.mark.asyncio
    async def test_update_status(
        self, client: AsyncClient, sample_threat: Threat
    ):
        resp = await client.patch(
            f"/api/v1/threats/{sample_threat.id}/status",
            json={"status": "VERIFIED"},
            headers={"X-API-Key": "sharkfin-demo-key-2026"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "VERIFIED"

    @pytest.mark.asyncio
    async def test_update_unauthorized(self, client: AsyncClient, sample_threat: Threat):
        resp = await client.patch(
            f"/api/v1/threats/{sample_threat.id}/status",
            json={"status": "VERIFIED"},
        )
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_update_not_found(self, client: AsyncClient):
        fake_id = uuid.uuid4()
        resp = await client.patch(
            f"/api/v1/threats/{fake_id}/status",
            json={"status": "VERIFIED"},
            headers={"X-API-Key": "sharkfin-demo-key-2026"},
        )
        assert resp.status_code == 404


class TestStatsSummary:
    @pytest.mark.asyncio
    async def test_empty_stats(self, client: AsyncClient):
        resp = await client.get("/api/v1/stats/summary")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_threats"] == 0
        assert "by_severity" in data
        assert "by_source" in data
        assert "institutions_mentioned" in data

    @pytest.mark.asyncio
    async def test_stats_with_data(
        self, client: AsyncClient, sample_threat: Threat
    ):
        resp = await client.get("/api/v1/stats/summary")
        data = resp.json()
        assert data["total_threats"] == 1
        assert data["by_severity"]["HIGH"] == 1
        assert data["by_source"]["TELEGRAM"] == 1
        assert "BRI" in data["institutions_mentioned"]


class TestResponseShape:
    @pytest.mark.asyncio
    async def test_threat_response_has_all_fields(
        self, client: AsyncClient, sample_threat: Threat
    ):
        resp = await client.get("/api/v1/threats")
        item = resp.json()["items"][0]
        required_fields = [
            "id", "source_type", "source_url", "content_preview",
            "detected_entities", "content_hash", "risk_score",
            "severity", "status", "institution_tags",
            "created_at", "updated_at",
        ]
        for field in required_fields:
            assert field in item, f"Missing field: {field}"
