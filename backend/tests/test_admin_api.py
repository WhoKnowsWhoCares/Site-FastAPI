"""Integration tests for admin API endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_content_requires_admin(client: AsyncClient):
    """Test that creating content requires admin auth."""
    payload = {
        "section": "aboutme",
        "content_type": "text",
        "title": "New Content",
        "body": "Body text",
    }
    response = await client.post("/api/admin/content", json=payload)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_content_success(client: AsyncClient, admin_token: str):
    """Test creating a content block as admin."""
    payload = {
        "section": "aboutme",
        "content_type": "text",
        "title": "Admin Created Content",
        "body": "Created via admin API",
        "order": 1,
        "is_published": True,
    }
    response = await client.post(
        "/api/admin/content",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Admin Created Content"
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_update_content_success(client: AsyncClient, admin_token: str):
    """Test updating a content block as admin."""
    # Create first
    create_resp = await client.post(
        "/api/admin/content",
        json={
            "section": "aboutme",
            "content_type": "text",
            "title": "Original Title",
            "body": "Original body",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    content_id = create_resp.json()["id"]

    # Update
    response = await client.put(
        f"/api/admin/content/{content_id}",
        json={"title": "Updated Title"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_update_content_not_found(client: AsyncClient, admin_token: str):
    """Test updating non-existent content returns 404."""
    response = await client.put(
        "/api/admin/content/99999",
        json={"title": "Nope"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_content_success(client: AsyncClient, admin_token: str):
    """Test deleting a content block as admin."""
    # Create first
    create_resp = await client.post(
        "/api/admin/content",
        json={
            "section": "aboutme",
            "content_type": "text",
            "title": "To Delete",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    content_id = create_resp.json()["id"]

    # Delete
    response = await client.delete(
        f"/api/admin/content/{content_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Content deleted successfully"


@pytest.mark.asyncio
async def test_delete_content_not_found(client: AsyncClient, admin_token: str):
    """Test deleting non-existent content returns 404."""
    response = await client.delete(
        "/api/admin/content/99999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_project_success(client: AsyncClient, admin_token: str):
    """Test creating a project as admin."""
    payload = {
        "section": "trade4me",
        "title": "New Project",
        "slug": "new-project",
        "description": "Project description",
    }
    response = await client.post(
        "/api/admin/project",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Project"
    assert data["slug"] == "new-project"


@pytest.mark.asyncio
async def test_update_project_success(client: AsyncClient, admin_token: str):
    """Test updating a project as admin."""
    # Create first
    create_resp = await client.post(
        "/api/admin/project",
        json={
            "section": "ihome",
            "title": "Original Project",
            "slug": "original-project",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    project_id = create_resp.json()["id"]

    response = await client.put(
        f"/api/admin/project/{project_id}",
        json={"title": "Updated Project"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Project"


@pytest.mark.asyncio
async def test_list_all_content_requires_admin(client: AsyncClient):
    """Test that listing all content requires admin auth."""
    response = await client.get("/api/admin/content")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_all_content_success(client: AsyncClient, admin_token: str):
    """Test listing all content as admin."""
    # Create some content first
    await client.post(
        "/api/admin/content",
        json={
            "section": "aboutme",
            "content_type": "text",
            "title": "List Item 1",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.get(
        "/api/admin/content",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_reorder_content(client: AsyncClient, admin_token: str):
    """Test reordering content blocks."""
    # Create two items
    r1 = await client.post(
        "/api/admin/content",
        json={"section": "aboutme", "content_type": "text", "title": "First"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    r2 = await client.post(
        "/api/admin/content",
        json={"section": "aboutme", "content_type": "text", "title": "Second"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    id1 = r1.json()["id"]
    id2 = r2.json()["id"]

    response = await client.post(
        "/api/admin/content/reorder",
        json={
            "section": "aboutme",
            "content_orders": [
                {"content_id": id1, "order": 10},
                {"content_id": id2, "order": 5},
            ],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Content reordered successfully"
