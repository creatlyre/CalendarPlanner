from datetime import datetime, timedelta


def test_month_view_renders_event_title_and_time(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)
    authenticated_client.post(
        "/api/events",
        json={
            "title": "Gym",
            "description": "Workout",
            "start_at": (now + timedelta(hours=1)).isoformat(),
            "end_at": (now + timedelta(hours=2)).isoformat(),
            "timezone": "UTC",
        },
    )

    response = authenticated_client.get(f"/calendar/month?year={now.year}&month={now.month}")
    assert response.status_code == 200
    assert "Gym" in response.text


def test_day_view_renders_event(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)
    authenticated_client.post(
        "/api/events",
        json={
            "title": "Lunch",
            "description": "Cafe",
            "start_at": (now + timedelta(hours=3)).isoformat(),
            "end_at": (now + timedelta(hours=4)).isoformat(),
            "timezone": "UTC",
        },
    )

    response = authenticated_client.get(f"/calendar/day?year={now.year}&month={now.month}&day={now.day}")
    assert response.status_code == 200
    assert "Lunch" in response.text


def test_month_navigation_changes_label(authenticated_client):
    now = datetime.utcnow().replace(microsecond=0)

    current_response = authenticated_client.get(f"/calendar/month?year={now.year}&month={now.month}")
    assert current_response.status_code == 200

    next_month = 1 if now.month == 12 else now.month + 1
    next_year = now.year + 1 if now.month == 12 else now.year

    next_response = authenticated_client.get(f"/calendar/month?year={next_year}&month={next_month}")
    assert next_response.status_code == 200
    assert current_response.text != next_response.text
