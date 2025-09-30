# scope-agent

Agent for structured budget search scoping — manages conversation state, clarifications, and generates reliable `[topic] [year]` queries.

---

## Overview

This project implements a **Budget Search Agent** responsible for:

- Scoping user requests (detecting topic and year)
- Asking clarifying questions if needed
- Generating structured budget search queries in the format `[topic] [year]`
- Persisting conversations in Redis
- Serving via a FastAPI interface for programmatic access

The agent is modular, allowing future addition of other agents under the same repository.

---

## Workflow

The budget search agent follows this workflow:

```mermaid
flowchart TD
    A[User sends request] --> B{Has topic & year?}
    B -- No --> C[Clarify with user]
    C --> B
    B -- Yes --> D[Generate structured budget search query]
    D --> E[Store conversation in Redis]
    E --> F[Return search query to user]
