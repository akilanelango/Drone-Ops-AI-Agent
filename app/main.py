from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import OpsAgent

# -------------------------
# APP SETUP
# -------------------------

app = FastAPI(
    title="Drone Operations Coordinator Agent",
    description="AI agent for coordinating pilots, drones, and missions",
    version="1.0.0",
)

# -------------------------
# LOAD AGENT ON STARTUP
# -------------------------

agent = OpsAgent(
    pilot_csv="data/pilot_roster.csv",
    drone_csv="data/drone_fleet.csv",
    mission_csv="data/missions.csv",
)

# -------------------------
# REQUEST / RESPONSE MODELS
# -------------------------

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


# -------------------------
# ROUTES
# -------------------------

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Drone Ops Agent is running."}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = agent.handle(request.message)
    return ChatResponse(response=reply)
