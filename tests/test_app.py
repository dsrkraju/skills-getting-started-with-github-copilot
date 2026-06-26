import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_them_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    initial_participants = list(activities[activity_name]["participants"])
    assert email in initial_participants

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]

    # Restore state for the rest of the test run
    activities[activity_name]["participants"] = initial_participants


def test_unregister_participant_returns_404_when_not_found():
    response = client.delete("/activities/Chess Club/participants/not-a-student@example.com")

    assert response.status_code == 404
