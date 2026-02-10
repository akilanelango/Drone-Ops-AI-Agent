# **📘 DECISION LOG**

**Project:** Drone Operations Coordinator AI Agent  
 **Author:** Akilan Elango  
 **Timeline:** \~6 hours

---

## **1\. Problem Interpretation**

The objective was to design an AI agent capable of handling the core responsibilities of a drone operations coordinator, including pilot roster management, drone inventory tracking, assignment coordination, conflict detection, and urgent reassignment handling.

Rather than interpreting “AI agent” as a machine learning model, I interpreted it as an **operations reasoning agent** that:

* Maintains system state

* Reasons deterministically over real operational constraints

* Explains its decisions clearly

This interpretation aligns with the problem’s emphasis on coordination, conflict handling, and explainability rather than prediction accuracy.

---

## **2\. Key Assumptions**

Given incomplete and evolving data specifications, the following assumptions were made:

* Each mission requires **one pilot and one drone**

* A pilot or drone can only be assigned to **one active mission at a time**

* External CSV data sources are **unreliable and schema-variant**

* Availability is determined by explicit status fields and current assignments

* Location mismatches are operational risks, not hard blockers

* If automation fails during urgent scenarios, the system must **escalate clearly**

All assumptions were documented in code and handled defensively.

---

## **3\. Data Modeling Decisions**

Instead of operating directly on CSV rows, the system converts all external data into validated domain models:

* `Pilot`

* `Drone`

* `Mission`

* `Assignment` (implicit)

This separation ensures:

* Clean reasoning logic

* Isolation of messy external data

* Easier conflict detection and reassignment

Pydantic models were chosen for clarity, validation, and FastAPI compatibility.

---

## **4\. Handling Schema Mismatch**

The provided CSVs differed significantly from the indicative schemas described in the problem statement.

Rather than modifying source data, the ingestion layer was designed to:

* Adapt dynamically to available columns

* Derive identifiers safely

* Fail gracefully on missing fields

This approach reflects real-world operations where upstream data contracts are often inconsistent.

---

## **5\. Conflict Detection Design**

Conflicts are classified into two categories:

### **Blocking Conflicts**

* Pilot or drone already assigned to overlapping missions

* Pilot lacking required certifications or skills

* Drone unavailable or under maintenance

### **Warnings**

* Pilot or drone location mismatches

This distinction allows the system to surface risks without unnecessarily blocking operations, reflecting real-world decision-making.

---

## **6\. Urgent Reassignment Strategy**

Urgent reassignment was treated as an optimization problem under constraints.

When a pilot becomes unavailable:

* The system evaluates all potential replacements

* Candidates are ranked using deterministic heuristics:

  * Same location

  * Skill overlap

  * Certification overlap

* The least disruptive option is selected

* If no valid alternative exists, the system escalates clearly

This avoids opaque or probabilistic decision-making while remaining explainable.

---

## **7\. Technology Choices**

* **Python \+ FastAPI:** Lightweight, expressive, production-grade

* **Pandas:** Reliable CSV ingestion and normalization

* **No database:** In-memory state was sufficient for the prototype scope

* **No ML models:** Deterministic logic prioritized explainability and correctness

---

## **8\. What I Would Improve With More Time**

* Persistent storage (PostgreSQL)

* Real Google Sheets API integration

* More advanced reassignment optimization

* Multi-mission planning and scheduling

* Authentication and role-based access

* UI dashboard for operations staff

---

## **9\. Summary**

The system prioritizes clarity, robustness, and explainability over complexity.  
 It demonstrates how an AI agent can reduce coordination overhead without introducing operational risk.

---

