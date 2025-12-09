import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_for_activity():
    # Use a test email and a known activity
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    # Ensure signup works
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response_dup.status_code == 400
    assert "already signed up" in response_dup.json()["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/invalid_activity/signup?email=someone@example.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
