from datetime import datetime, timedelta


def test_create_event_then_day_panel_contains_it(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)
    start = now.replace(hour=10, minute=0, second=0)
    end = now.replace(hour=11, minute=0, second=0)

    create_response = authenticated_client.post(
        "/api/events",
        json={
            "title": "Dentist",
            "description": "Checkup",
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "timezone": "UTC",
        },
    )
    assert create_response.status_code == 201

    day_response = authenticated_client.get(
        f"/calendar/day?year={start.year}&month={start.month}&day={start.day}"
    )
    assert day_response.status_code == 200
    assert "Dentist" in day_response.text


def test_update_then_delete_flow(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)

    create_response = authenticated_client.post(
        "/api/events",
        json={
            "title": "Temp Event",
            "description": None,
            "start_at": (now + timedelta(hours=1)).isoformat(),
            "end_at": (now + timedelta(hours=2)).isoformat(),
            "timezone": "UTC",
        },
    )
    event_id = create_response.json()["id"]

    update_response = authenticated_client.put(
        f"/api/events/{event_id}", json={"title": "Permanent Event"}
    )
    assert update_response.status_code == 200

    month_response = authenticated_client.get(
        f"/calendar/month?year={now.year}&month={now.month}"
    )
    assert "Permanent Event" in month_response.text

    delete_response = authenticated_client.delete(f"/api/events/{event_id}")
    assert delete_response.status_code == 200

    month_response_after_delete = authenticated_client.get(
        f"/api/events/month?year={now.year}&month={now.month}"
    )
    assert all(item["id"] != event_id for item in month_response_after_delete.json())
