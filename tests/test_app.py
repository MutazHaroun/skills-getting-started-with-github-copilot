from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_catalog():
    # Arrange
    # No special setup needed for this endpoint.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Art Club"
    email = "backend-test@mergington.edu"
    original_participants = list(activities[activity_name]["participants"])

    try:
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_duplicate_signup_returns_400():
    # Arrange
    activity_name = "Art Club"
    email = "ava@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400


def test_unregister_participant_removes_email():
    # Arrange
    activity_name = "Art Club"
    email = "ava@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]

    activities[activity_name]["participants"].append(email)


def test_unregister_unknown_participant_returns_404():
    # Arrange
    # The participant does not exist in the sample data.

    # Act
    response = client.delete("/activities/Art Club/signup?email=missing@mergington.edu")

    # Assert
    assert response.status_code == 404
