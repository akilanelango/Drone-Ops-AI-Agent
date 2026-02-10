# **Drone Operations Coordinator AI Agent**

A conversational AI agent designed to coordinate pilots, drones, and missions for multi-project drone operations.

The system replaces manual coordination across spreadsheets and messages with a single explainable agent capable of managing availability, assignments, conflicts, and urgent reassignments.

---

## **🚀 Features**

* Conversational interface (`/chat`)  
* Pilot roster management  
* Drone inventory tracking  
* Assignment coordination  
* Conflict detection (blocking vs warnings)  
* Urgent reassignment handling  
* Explainable decision-making  
* Interactive Swagger UI for testing

---

## **🧠 System Architecture**

app/  
├── main.py — FastAPI entrypoint  
├── agent.py — Conversational agent logic  
├── models.py — Domain models (Pilot, Drone, Mission)  
├── data\_loader.py — CSV ingestion and normalization  
├── conflict\_detector.py — Conflict detection engine  
├── urgency.py — Urgent reassignment logic

data/  
├── pilot\_roster.csv  
├── drone\_fleet.csv  
├── missions.csv

---

## **🛠️ Tech Stack**

* Python 3.10  
* FastAPI  
* Pydantic  
* Pandas  
* Uvicorn

The system uses deterministic logic rather than machine learning models in order to prioritize correctness, explainability, and operational safety.

---

## **🧪 Running Locally**

1. Create and activate a virtual environment  
2. Install dependencies  
3. Start the server

The application runs at:

* Health check: http://127.0.0.1:8000  
* Swagger UI: http://127.0.0.1:8000/docs

---

## **💬 Example Chat Queries**

Which pilots are available?  
Which drones are available?  
Assign a mission  
urgent reassignment

---

## **⚠️ Conflict Detection**

The agent detects and classifies conflicts before assignments are made.

**Blocking conflicts**

* Pilot assigned to overlapping missions  
* Pilot lacks required skills or certifications  
* Drone unavailable or in maintenance

**Warnings**

* Pilot location differs from mission location  
* Drone location differs from mission location

Warnings do not block assignments but surface operational risk for human awareness.

---

## **🚨 Urgent Reassignment Logic**

When an urgent failure occurs (for example, a pilot becomes unavailable mid-mission), the agent:

1. Identifies the impacted mission  
2. Evaluates available standby pilots  
3. Ranks candidates based on:  
   * Location match  
   * Skill overlap  
   * Certification overlap  
4. Selects the least disruptive option  
5. Explains the decision  
6. Escalates clearly if no valid reassignment exists

This ensures predictable and explainable emergency handling.

---

## **🌍 Deployment**

The agent is deployed as a hosted FastAPI service on **Hugging Face Spaces**, providing:

* Public access via URL  
* No local setup for reviewers  
* Interactive Swagger UI for live testing

---

## **📌 Design Philosophy**

* Explainability over opacity  
* Deterministic behavior over probabilistic guesses  
* Defensive ingestion of external data  
* Real-world operations realism

---

## **🏁 Conclusion**

This project demonstrates how an AI agent can function as an operations coordinator, reducing manual overhead while maintaining transparency, safety, and control in complex, high-coordination environments.

---

