from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Art Club"
    email = "ava@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]

    # Restore state for future runs
    activities[activity_name]["participants"].append(email)


def test_unregister_unknown_participant_returns_404():
    response = client.delete("/activities/Art Club/signup?email=missing@mergington.edu")

    assert response.status_code == 404
