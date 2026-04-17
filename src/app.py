"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": { ... },
    "Programming Class": { ... },
    "Gym Class": { ... },

    # Sports
    "Soccer Team": {
        "description": "Practice team tactics and play matches on the school field",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Volleyball Club": {
        "description": "Learn volleyball skills and compete in friendly games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": []
    },

    # Artistic
    "Art Studio": {
        "description": "Explore painting, drawing, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Drama Club": {
        "description": "Rehearse scenes, improvise, and prepare for a school play",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": []
    },

    # Intellectual
    "Debate Society": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": []
    },
    "Science Olympiad": {
        "description": "Work on science challenges and prepare for regional competitions",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

# Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")                        
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/signup")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student not signed up")

    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
