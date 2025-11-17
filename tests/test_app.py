from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # spot-check a known activity and participant
    assert "Chess Club" in data
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test-user@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Unregister
    delete_resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert delete_resp.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent_participant():
    activity = "Chess Club"
    email = "nonexistent@example.com"

    # Ensure not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    delete_resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert delete_resp.status_code == 404
