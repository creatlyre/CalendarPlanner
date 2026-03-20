"""PERF-01, PERF-02, and PERF-03: Performance optimization validation tests."""
import pathlib

from fastapi.testclient import TestClient

from main import app


class TestNoCDN:
    """PERF-01: No pages load the Tailwind CDN play script."""

    def test_base_template_has_no_cdn_script(self):
        """Verify base.html references static CSS, not CDN."""
        base_html = pathlib.Path("app/templates/base.html").read_text(encoding="utf-8")
        assert "cdn.tailwindcss.com" not in base_html
        assert "play.tailwindcss.com" not in base_html
        assert "unpkg.com/tailwind" not in base_html

    def test_base_template_uses_static_css(self):
        """Verify base.html links to prebuilt static CSS file."""
        base_html = pathlib.Path("app/templates/base.html").read_text(encoding="utf-8")
        assert "/static/css/style.css" in base_html

    def test_no_cdn_in_any_template(self):
        """Verify no template file references Tailwind CDN."""
        templates_dir = pathlib.Path("app/templates")
        cdn_patterns = ["cdn.tailwindcss.com", "play.tailwindcss.com"]
        for template in templates_dir.rglob("*.html"):
            content = template.read_text(encoding="utf-8")
            for pattern in cdn_patterns:
                assert pattern not in content, f"CDN reference found in {template}: {pattern}"

    def test_prebuilt_css_file_exists(self):
        """Verify the prebuilt CSS file exists and is non-empty."""
        css_path = pathlib.Path("public/css/style.css")
        assert css_path.exists(), "Prebuilt CSS file missing"
        assert css_path.stat().st_size > 1000, "CSS file suspiciously small"


class TestConnectionPooling:
    """PERF-02: SupabaseStore reuses httpx connections across requests."""

    def test_shared_client_singleton(self):
        """Verify _get_shared_client returns the same instance."""
        from app.database.supabase_store import _get_shared_client, _shared_client
        import app.database.supabase_store as store_module

        # Reset to test fresh creation
        store_module._shared_client = None

        client1 = _get_shared_client()
        client2 = _get_shared_client()
        assert client1 is client2, "Connection pooling: clients should be same instance"

        # Cleanup
        client1.close()
        store_module._shared_client = None

    def test_supabase_store_instances_share_client(self):
        """Verify two SupabaseStore instances share the same httpx.Client."""
        import app.database.supabase_store as store_module

        store_module._shared_client = None

        s1 = store_module.SupabaseStore()
        s2 = store_module.SupabaseStore()
        assert s1._client is s2._client, "SupabaseStore instances must share client"

        # Cleanup
        s1._client.close()
        store_module._shared_client = None


class TestCacheControlHeaders:
    """PERF-03: Static CSS file served with Cache-Control headers."""

    def test_static_css_has_cache_control(self):
        """Verify /static/css/style.css response includes Cache-Control header."""
        client = TestClient(app)
        resp = client.get("/static/css/style.css")
        assert resp.status_code == 200
        assert "Cache-Control" in resp.headers
        assert "public" in resp.headers["Cache-Control"]
        assert "max-age=604800" in resp.headers["Cache-Control"]

    def test_non_static_route_no_cache_header(self):
        """Verify Cache-Control is NOT added to non-static routes."""
        client = TestClient(app)
        resp = client.get("/", follow_redirects=False)
        cache = resp.headers.get("Cache-Control", "")
        assert "max-age=604800" not in cache
