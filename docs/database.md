# Database Design

## Current Implementation (MVP)

CuraLens AI's current backend uses **SQLite** via SQLAlchemy, not
Firestore. Two tables exist today:

**`users`** — id, name, email, password (hashed), is_verified, otp

**`prescriptions`** — id, user_id (FK), patient_name, doctor_name,
hospital, medicine_count, risk_level, score, result_json (the full
analysis result, stored as JSON), created_at

This is intentionally minimal for the hackathon MVP: every analyzed
prescription is saved against the logged-in user, and viewable again
later from the History page without re-running OCR/AI.

---

## Planned Architecture (Future / Not Yet Implemented)

The sections below describe the originally planned Firestore-based
design for a full production version - reminders, medication
adherence tracking, per-agent logging, and feedback collection. None
of this is implemented yet; it's included here as the intended
direction for scaling beyond the hackathon MVP.

## Overview

CuraLens AI uses **Firebase Firestore** as the primary NoSQL database and **Firebase Storage** for prescription images.

The database is designed to:

- Store patient profiles securely
- Store uploaded prescriptions
- Store extracted medicine details separately
- Support AI agent workflows
- Generate medication reminders
- Track medication adherence
- Scale for future hospital integrations

---

# Database Architecture

```
Firestore
│
├── users
│
├── prescriptions
│
├── medicines
│
├── reminders
│
├── medication_history
│
├── ai_logs
│
└── feedback
```

---

# Entity Relationship Diagram (ERD)

```
                 ┌──────────────┐
                 │    USERS     │
                 └──────┬───────┘
                        │
                        │ 1 User
                        │
                        ▼
             ┌────────────────────┐
             │  PRESCRIPTIONS     │
             └─────────┬──────────┘
                       │
       One Prescription│contains many
                       ▼
              ┌────────────────┐
              │   MEDICINES    │
              └────────┬───────┘
                       │
                       │
              ┌────────┴───────────┐
              ▼                    ▼
        REMINDERS         MEDICATION_HISTORY

```

**Relationship**

```
One User
    │
    ├── Many Prescriptions

One Prescription
    │
    ├── Many Medicines

One Medicine
    │
    ├── Many Reminders

One Reminder
    │
    └── One Medication History
```

---

# Collection 1 : Users

Stores patient profile information.

```
users
```

| Field | Type | Description |
|-------|------|-------------|
| userId | String | Unique User ID |
| fullName | String | Patient Name |
| age | Number | Age |
| gender | String | Gender |
| phone | String | Contact Number |
| preferredLanguage | String | English / Kannada / Hindi |
| createdAt | Timestamp | Registration Time |

Example

```json
{
  "userId":"USR001",
  "fullName":"Lakshmi",
  "age":56,
  "gender":"Female",
  "phone":"9876543210",
  "preferredLanguage":"Kannada"
}
```

---

# Collection 2 : Prescriptions

Each uploaded prescription is stored as a separate document.

```
prescriptions
```

| Field | Type |
|------|------|
| prescriptionId | String |
| userId | String |
| imageUrl | String |
| uploadDate | Timestamp |
| processingStatus | String |
| extractedText | String |

Status

- Uploaded
- Processing
- Verified
- Completed

Example

```json
{
    "prescriptionId":"P001",
    "userId":"USR001",
    "imageUrl":"firebase-url",
    "processingStatus":"Verified"
}
```

---

# Collection 3 : Medicines

**Important**

Medicines are NOT stored inside the prescription document.

Each medicine becomes its own Firestore document.

This allows:

- Editing one medicine
- AI verification
- Individual reminders
- Future interaction analysis

```
prescription
        │
        ├── Medicine 1
        ├── Medicine 2
        ├── Medicine 3
```

Collection

```
medicines
```

| Field | Type |
|------|------|
| medicineId | String |
| prescriptionId | String |
| medicineName | String |
| dosage | String |
| frequency | String |
| duration | String |
| timing | String |
| foodInstruction | String |
| confidenceScore | Number |
| verificationStatus | String |

Example

```json
{
  "medicineId":"MED001",
  "prescriptionId":"P001",
  "medicineName":"Paracetamol",
  "dosage":"650 mg",
  "frequency":"Twice Daily",
  "duration":"5 Days",
  "timing":"Morning, Night",
  "foodInstruction":"After Food",
  "confidenceScore":0.96,
  "verificationStatus":"Verified"
}
```

---

# Collection 4 : Reminders

Every medicine can have multiple reminders.

```
Medicine

│

├── 8:00 AM

├── 2:00 PM

└── 8:00 PM
```

Collection

```
reminders
```

| Field | Type |
|------|------|
| reminderId | String |
| medicineId | String |
| reminderTime | Timestamp |
| status | String |

Status

- Pending
- Taken
- Missed
- Snoozed

---

# Collection 5 : Medication History

Tracks adherence.

```
medication_history
```

| Field | Type |
|------|------|
| historyId | String |
| reminderId | String |
| action | String |
| timestamp | Timestamp |

Actions

- Taken
- Missed
- Snoozed

---

# Collection 6 : AI Logs

Stores outputs from each AI agent for debugging and explainability.

```
ai_logs
```

| Field | Type |
|------|------|
| logId | String |
| prescriptionId | String |
| agentName | String |
| input | Map |
| output | Map |
| processingTime | Number |
| createdAt | Timestamp |

Example

```
Vision Agent

↓

Medicine Extraction

↓

Verification Agent

↓

Medication Intelligence Agent

↓

Safety Agent

↓

Reminder Agent
```

---

# Collection 7 : Feedback

Stores patient feedback.

```
feedback
```

| Field | Type |
|------|------|
| feedbackId | String |
| userId | String |
| rating | Number |
| comments | String |
| createdAt | Timestamp |

---

# Why Separate Medicines?

Instead of storing all medicines inside one prescription document:

```
Prescription

↓

Medicine 1

Medicine 2

Medicine 3
```

We store each medicine independently because it enables:

- Individual AI verification
- Separate reminder generation
- Easy medicine updates
- Drug interaction checks
- Better scalability
- Cleaner Firestore queries

This follows a scalable NoSQL design while avoiding oversized prescription documents.

---

# Security

- Firebase Authentication for user identity
- Firestore Security Rules
- Firebase Storage for prescription images
- Secure API keys
- HTTPS communication
- User-level access control

---

# Future Collections

Future versions may include:

- doctors
- hospitals
- caregivers
- multilingual_translations
- voice_logs
- analytics
- hospital_notifications

---

# Database Summary

```
Users
   │
   ├──────────────┐
   ▼              ▼
Prescriptions   Feedback
      │
      ▼
Medicines
      │
      ▼
Reminders
      │
      ▼
Medication History

AI Logs (Generated by every AI Agent)
```

---

## Design Principles

- Modular
- Scalable
- Agent-friendly
- Explainable
- Easy to maintain
- Ready for future hospital integration