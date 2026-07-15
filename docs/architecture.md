# System Architecture

## Current Implementation Note

This document describes the original planned architecture. Two
things differ in the current MVP build:

- **Orchestration** is a custom Python `AgentManager` class
  (`app/orchestrator/agent_manager.py`), not the Google Agent
  Development Kit (ADK). It performs the same job (coordinating
  agent handoffs) but isn't built on Google's ADK library.
- **Storage** is SQLite via SQLAlchemy (`users` and `prescriptions`
  tables), not Firebase/Firestore.

Gemini usage (section 3 below) is accurate as-is - both OCR and
medicine explanations run on Gemini 2.5 Flash.

## Overview

CuraLens AI is a cloud-based, multi-agent medication guidance platform that uses Google's AI ecosystem to convert handwritten prescriptions into clear, multilingual, and actionable medication guidance.

The system follows a modular architecture where each component has a well-defined responsibility.

---

# High-Level Architecture

```
                        ┌────────────────────┐
                        │      Patient       │
                        └─────────┬──────────┘
                                  │
                                  ▼
                     Upload Prescription Image
                                  │
                                  ▼
                  ┌────────────────────────────┐
                  │      React Frontend        │
                  └─────────┬──────────────────┘
                            │ REST API
                            ▼
                 ┌─────────────────────────────┐
                 │      FastAPI Backend        │
                 └─────────┬───────────────────┘
                           │
          ┌────────────────┼──────────────────┐
          ▼                ▼                  ▼
    Google Gemini     Python AgentManager     SQLite
    (Vision + LLM)     (custom orchestrator)   DB
          │
          ▼
    Multi-Agent Workflow
          │
          ▼
   Structured Medication Plan
          │
          ▼
   Patient Dashboard & History
```

---

# System Components

## 1. Frontend

Technology:
- React
- Vite
- Tailwind CSS

Responsibilities:

- Upload prescription images
- Display extracted medicines
- Show AI explanations
- Display medication schedule
- Display reminder timeline

---

## 2. Backend

Technology:

- FastAPI

Responsibilities:

- Receive uploaded images
- Call Gemini APIs
- Execute AI agents
- Manage patient data
- Return structured responses

---

## 3. Gemini AI

Technology:

- Gemini Vision
- Gemini 2.5 Flash

Responsibilities:

- Read handwritten prescriptions
- Extract medicine details
- Generate explanations
- Translate instructions

---

## 4. Agent Orchestrator

Technology:

- Custom Python `AgentManager` class (not Google ADK)

Responsibilities:

- Orchestrate AI agents
- Pass data between agents
- Manage agent workflow

*(Originally planned to use Google ADK - current MVP uses a custom
orchestrator instead. Adopting ADK is a possible future improvement.)*

---

## 5. Storage (Current: SQLite)

Current implementation:

- SQLite via SQLAlchemy
- Tables: `users`, `prescriptions`

Responsibilities:

- Store prescription analysis results
- User authentication (basic - JWT session tokens not yet implemented)

*(Originally planned as Firebase/Firestore for the reasons described
in database.md - see that file's "Planned Architecture" section for
the full future-state design.)*

---

# Multi-Agent Workflow

```
Prescription Image
        │
        ▼
Vision Agent (Gemini OCR)
        │
        ▼
Verification Agent (database match)
        │
        ▼
Medication Agent (Gemini explanations)
        │
        ▼
Safety Agent (interaction checks)
        │
        ▼
Score Agent
        │
        ▼
Dashboard
```

*(Reminder Agent is planned but not yet implemented.)*

---

# Data Flow

```
Patient

↓

Upload Image

↓

Frontend

↓

FastAPI

↓

Gemini Vision

↓

AI Agents

↓

Medication Plan

↓

SQLite (saved to History)

↓

Dashboard
```

---

# Security Considerations

- Secure image upload
- Firebase Authentication
- HTTPS communication
- Input validation
- Secure API key storage
- User data isolation

---

# Scalability

The architecture is designed so each component can scale independently.

Examples:

- More AI agents can be added.
- Multiple languages can be supported.
- Hospital integration can be introduced.
- Mobile applications can consume the same backend APIs.

---

# Future Architecture Enhancements

- Voice Agent
- Hospital Information System Integration
- Offline Synchronization
- Doctor Portal
- Caregiver Dashboard
- Analytics Dashboard