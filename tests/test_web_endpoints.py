# Tests for Flask web endpoints

import json

from web.app import create_app


def test_health_endpoint():
    app = create_app()
    client = app.test_client()

    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("status") == "ok"
    assert "uptime_seconds" in data


def test_index_and_reference_pages():
    app = create_app()
    client = app.test_client()

    idx = client.get("/")
    assert idx.status_code == 200
    assert "<" in idx.get_data(as_text=True)

    ref = client.get("/reference")
    assert ref.status_code == 200
    assert "<" in ref.get_data(as_text=True)


def test_api_check_requires_firebase_disabled():
    app = create_app()
    client = app.test_client()

    # Server may be configured for Firebase in this environment; accept 500 (not configured)
    # or 401 (configured but missing Authorization header).
    resp = client.post(
        "/api/check",
        data=json.dumps({"source": "OUTPUT 1"}),
        content_type="application/json",
    )
    assert resp.status_code in (500, 401)
    data = resp.get_json()
    assert data.get("ok") is False


def test_api_examples_list_and_get():
    app = create_app()
    client = app.test_client()

    resp = client.get("/api/examples")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data.get("examples"), list)

    # Pick a known example file
    if data.get("examples"):
        name = data.get("examples")[0]
        r = client.get(f"/api/examples/{name}")
        assert r.status_code == 200
        d = r.get_json()
        assert d.get("name") == name
        assert "source" in d
