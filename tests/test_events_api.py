from datetime import datetime, timedelta


def _payload(title: str, start: datetime, end: datetime) -> dict:
    return {
        "title": title,
        "description": "desc",
        "start_at": start.isoformat(),
        "end_at": end.isoformat(),
        "timezone": "UTC",
    }


def test_create_event(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)
    response = authenticated_client.post(
        "/api/events",
        json=_payload("Doctor", now + timedelta(hours=1), now + timedelta(hours=2)),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"]
    assert data["title"] == "Doctor"


def test_update_event(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)
    create_response = authenticated_client.post(
        "/api/events",
        json=_payload("Initial", now + timedelta(hours=1), now + timedelta(hours=2)),
    )
    event_id = create_response.json()["id"]

    update_response = authenticated_client.put(
        f"/api/events/{event_id}",
        json={"title": "Updated Title"},
    )

    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"


def test_delete_event_hides_from_month(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)
    create_response = authenticated_client.post(
        "/api/events",
        json=_payload("Temporary", now + timedelta(hours=1), now + timedelta(hours=2)),
    )
    event_id = create_response.json()["id"]

    delete_response = authenticated_client.delete(f"/api/events/{event_id}")
    assert delete_response.status_code == 200

    month_response = authenticated_client.get(f"/api/events/month?year={now.year}&month={now.month}")
    assert month_response.status_code == 200
    ids = [item["id"] for item in month_response.json()]
    assert event_id not in ids
