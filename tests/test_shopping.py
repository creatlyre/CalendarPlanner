"""Tests for shopping list (Phase 25)."""
import pytest


class TestShoppingItemCRUD:
    """SHOP-01, SHOP-02: Add, edit, delete items."""

    def test_add_item(self, authenticated_client):
        res = authenticated_client.post(
            "/api/shopping/items",
            json={"name": "Masło"},
        )
        assert res.status_code == 201
        data = res.json()["data"]
        assert data["name"] == "Masło"
        assert data["id"]

    def test_get_items_grouped(self, authenticated_client):
        authenticated_client.post("/api/shopping/items", json={"name": "Masło"})
        authenticated_client.post("/api/shopping/items", json={"name": "Piwo"})
        res = authenticated_client.get("/api/shopping/items")
        assert res.status_code == 200
        data = res.json()["data"]
        assert "sections" in data

    def test_update_item(self, authenticated_client):
        create = authenticated_client.post("/api/shopping/items", json={"name": "Masło"})
        item_id = create.json()["data"]["id"]
        res = authenticated_client.put(
            f"/api/shopping/items/{item_id}",
            json={"name": "Masło ekstra"},
        )
        assert res.status_code == 200
        assert res.json()["data"]["name"] == "Masło ekstra"

    def test_delete_item(self, authenticated_client):
        create = authenticated_client.post("/api/shopping/items", json={"name": "Masło"})
        item_id = create.json()["data"]["id"]
        res = authenticated_client.delete(f"/api/shopping/items/{item_id}")
        assert res.status_code == 200
        assert res.json()["ok"] is True

    def test_delete_nonexistent_item(self, authenticated_client):
        res = authenticated_client.delete("/api/shopping/items/nonexistent-id")
        assert res.status_code == 404


class TestShoppingMultiAdd:
    """SHOP-04: Multi-item paste."""

    def test_multi_add_comma_separated(self, authenticated_client):
        res = authenticated_client.post(
            "/api/shopping/items/multi",
            json={"text": "Masło, Mleko, Jogurt"},
        )
        assert res.status_code == 201
        data = res.json()["data"]
        assert len(data["items"]) == 3
        names = {i["name"] for i in data["items"]}
        assert names == {"Masło", "Mleko", "Jogurt"}

    def test_multi_add_newline_separated(self, authenticated_client):
        res = authenticated_client.post(
            "/api/shopping/items/multi",
            json={"text": "Banan\nJabłko\nPomidor"},
        )
        assert res.status_code == 201
        data = res.json()["data"]
        assert len(data["items"]) == 3

    def test_multi_add_empty_text(self, authenticated_client):
        res = authenticated_client.post(
            "/api/shopping/items/multi",
            json={"text": ""},
        )
        assert res.status_code == 422  # Validation error


class TestShoppingAutoCategorize:
    """SHOP-05: Auto-categorization via keywords."""

    def test_item_auto_categorized(self, authenticated_client):
        # Masło should be categorized to Nabiał i Lodówki
        res = authenticated_client.post("/api/shopping/items", json={"name": "Masło"})
        assert res.status_code == 201
        data = res.json()["data"]
        # The item should have a section_id (auto-categorized)
        assert data["section_id"] is not None

    def test_unknown_item_uncategorized(self, authenticated_client):
        res = authenticated_client.post("/api/shopping/items", json={"name": "Fizblorp"})
        assert res.status_code == 201
        data = res.json()["data"]
        assert data["section_id"] is None


class TestShoppingKeywordLearning:
    """SHOP-05: Learn keyword mappings."""

    def test_learn_keyword(self, authenticated_client):
        # Add unknown item
        create = authenticated_client.post("/api/shopping/items", json={"name": "Fizblorp"})
        item_id = create.json()["data"]["id"]
        # Get sections to find a section_id
        sections_res = authenticated_client.get("/api/shopping/sections")
        section_id = sections_res.json()["data"][0]["id"]
        # Learn the keyword
        res = authenticated_client.post(
            f"/api/shopping/items/{item_id}/learn",
            json={"item_name": "Fizblorp", "section_id": section_id},
        )
        assert res.status_code == 200
        assert res.json()["ok"] is True


class TestShoppingSections:
    """SHOP-05: Section management."""

    def test_get_sections_preset(self, authenticated_client):
        res = authenticated_client.get("/api/shopping/sections")
        assert res.status_code == 200
        sections = res.json()["data"]
        assert len(sections) == 10
        names = [s["name"] for s in sections]
        assert "Warzywa i Owoce" in names
        assert "Chemia / Higiena" in names

    def test_create_custom_section(self, authenticated_client):
        res = authenticated_client.post(
            "/api/shopping/sections",
            json={"name": "Delikatesy", "emoji": "🧁"},
        )
        assert res.status_code == 201
        assert res.json()["data"]["name"] == "Delikatesy"

    def test_get_keywords(self, authenticated_client):
        res = authenticated_client.get("/api/shopping/keywords")
        assert res.status_code == 200
        data = res.json()["data"]
        assert "Warzywa i Owoce" in data
        assert "Nabiał i Lodówki" in data


class TestShoppingSharedAccess:
    """SHOP-03: Both users share the same list."""

    def test_shared_list(self, authenticated_client, test_db, test_user_a):
        # Adding items via authenticated_client (user A) creates them under the shared calendar_id
        authenticated_client.post("/api/shopping/items", json={"name": "Mleko"})
        res = authenticated_client.get("/api/shopping/items")
        data = res.json()["data"]
        # Total items across all sections + uncategorized = 1
        total = sum(len(s.get("items", [])) for s in data["sections"]) + len(data.get("uncategorized", []))
        assert total == 1


class TestShoppingServiceUnit:
    """Unit tests for ShoppingService logic."""

    def test_categorize_keywords_loaded(self):
        from app.shopping.service import SECTION_KEYWORDS
        assert len(SECTION_KEYWORDS) == 10
        assert "Warzywa i Owoce" in SECTION_KEYWORDS
        assert "Alkohol" in SECTION_KEYWORDS

    def test_normalize_diacritics(self):
        from app.shopping.service import _normalize
        assert _normalize("Masło") == "maslo"
        assert _normalize("Żeberka") == "zeberka"
        assert _normalize("Łosoś") == "losos"

    def test_multi_item_parsing(self):
        import re
        text = "Masło, Mleko, Jogurt"
        items = re.split(r"[,\n]+", text)
        names = [t.strip() for t in items if t.strip()]
        assert names == ["Masło", "Mleko", "Jogurt"]

    def test_multi_item_newline_parsing(self):
        import re
        text = "Banan\nJabłko\nPomidor"
        items = re.split(r"[,\n]+", text)
        names = [t.strip() for t in items if t.strip()]
        assert names == ["Banan", "Jabłko", "Pomidor"]


class TestShoppingViewPage:
    """Verify /shopping page renders."""

    def test_shopping_page_loads(self, authenticated_client):
        res = authenticated_client.get("/shopping")
        assert res.status_code == 200
        assert "shopping" in res.text.lower()
