"""Integration tests for health check endpoint."""

import pytest
from httpx import AsyncClient


class TestHealthAPI:
    """Tests for /health endpoint."""

    @pytest.mark.asyncio
    async def test_health_check_success(self, client: AsyncClient):
        """GET /health should return healthy status."""
        response = await client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "healthy"
        assert "database" in data["data"]
        assert data["data"]["database"] == "connected"

    @pytest.mark.asyncio
    async def test_health_check_response_format(self, client: AsyncClient):
        """GET /health should follow standard response format."""
        response = await client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()

        # Verify standard response format
        assert "success" in data
        assert "data" in data
        assert "timestamp" in data
        assert data["error"] is None

    @pytest.mark.asyncio
    async def test_health_check_no_auth_required(self, client: AsyncClient):
        """GET /health should not require authentication."""
        # No auth headers - should still succeed
        response = await client.get("/api/v1/health")

        assert response.status_code == 200
