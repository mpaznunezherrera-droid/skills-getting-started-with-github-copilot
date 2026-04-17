import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)

def test_root_redirect():
    # Arrange - nothing special needed
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    # Arrange - nothing special needed
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Soccer Team" in data
    # Check structure of one activity
    activity = data["Soccer Team"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)

def test_signup_success():
    # Arrange
    email = "student@example.com"
    activity_name = "Soccer Team"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    # Verify the student was added
    response2 = client.get("/activities")
    data2 = response2.json()
    assert email in data2[activity_name]["participants"]

def test_signup_already_signed_up():
    # Arrange
    email = "student@example.com"
    activity_name = "Soccer Team"
    client.post(f"/activities/{activity_name}/signup?email={email}")  # Sign up first
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()

def test_signup_activity_not_found():
    # Arrange
    email = "student@example.com"
    activity_name = "Nonexistent Activity"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()

def test_delete_success():
    # Arrange
    email = "student@example.com"
    activity_name = "Soccer Team"
    client.post(f"/activities/{activity_name}/signup?email={email}")  # Sign up first
    
    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    # Verify the student was removed
    response2 = client.get("/activities")
    data2 = response2.json()
    assert email not in data2[activity_name]["participants"]

def test_delete_not_signed_up():
    # Arrange
    email = "student@example.com"
    activity_name = "Soccer Team"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"].lower()

def test_delete_activity_not_found():
    # Arrange
    email = "student@example.com"
    activity_name = "Nonexistent Activity"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()