import pytest
from urllib.parse import quote


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_list(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity_adds_participant(client):
    email = "test.student@mergington.edu"
    activity_name = quote("Chess Club")
    response = client.post(f"/activities/{activity_name}/signup?email={quote(email)}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_remove_participant_from_activity(client):
    email = "michael@mergington.edu"
    response = client.delete(f"/activities/{quote('Chess Club')}/participants/{quote(email)}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email not in participants


def test_signup_for_unknown_activity_returns_404(client):
    response = client.post(f"/activities/{quote('Unknown Club')}/signup?email={quote('test@mergington.edu')}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_unknown_participant_returns_404(client):
    response = client.delete(
        f"/activities/{quote('Chess Club')}/participants/{quote('unknown.student@mergington.edu')}"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
