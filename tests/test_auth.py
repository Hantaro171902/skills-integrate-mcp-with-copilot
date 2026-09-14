from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unauthenticated_signup_is_rejected():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 401


def test_student_can_only_sign_up_for_their_own_email():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@mergington.edu"},
        auth=("student@mergington.edu", "studentpass"),
    )

    assert response.status_code == 200
    assert "Signed up student@mergington.edu for Chess Club" in response.json()["message"]

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "another@mergington.edu"},
        auth=("student@mergington.edu", "studentpass"),
    )

    assert response.status_code == 403


def test_admin_can_access_admin_endpoints():
    response = client.get(
        "/admin/activities",
        auth=("teacher@mergington.edu", "teacherpass"),
    )

    assert response.status_code == 200
    assert "Chess Club" in response.json()
