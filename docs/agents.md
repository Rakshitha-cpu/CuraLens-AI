# AI Agent Architecture

## Overview

CuraLens AI is built as a multi-agent system where each AI agent is responsible for a specific task in the medication guidance workflow.

Instead of one AI model performing every operation, specialized agents collaborate to provide accurate, explainable, and patient-friendly medication assistance.

---

# Agent Workflow

```
Patient
    │
    ▼
Upload Prescription
    │
    ▼
Vision Agent
    │
    ▼
Verification Agent
    │
    ▼
Medication Intelligence Agent
    │
    ▼
Safety Agent
    │
    ▼
Education Agent
    │
    ▼
Reminder Agent
    │
    ▼
Patient Dashboard
```

---

# 1. Vision Agent

## Purpose

Extract information from handwritten prescriptions.

## Responsibilities

- Read prescription image
- Detect medicine names
- Detect dosage
- Detect frequency
- Detect duration
- Detect instructions

## Input

Prescription Image

## Output

Structured prescription data

Example

```
Medicine:
Paracetamol 650 mg

Dosage:
1 Tablet

Frequency:
Twice Daily

Duration:
5 Days
```

---

# 2. Verification Agent

## Purpose

Validate extracted information.

## Responsibilities

- Detect low-confidence medicine names
- Highlight uncertain text
- Ask user for confirmation
- Prevent incorrect medicine interpretation

Example

Instead of assuming:

```
Metformin
```

Ask:

```
Did you mean

• Metformin
• Metronidazole
```

---

# 3. Medication Intelligence Agent

## Purpose

Explain medicines in simple language.

## Responsibilities

- Medicine purpose
- Dosage explanation
- Food instructions
- Duration explanation

Example

Medicine:
Amoxicillin

Purpose:
Treats bacterial infections.

Take:
After food.

Complete the full course.

---

# 4. Safety Agent

## Purpose

Improve medication safety.

## Responsibilities

- Detect duplicate medicines
- Detect missing dosage
- Detect common medicine interactions
- Highlight possible issues

Example

Warning:

Duplicate Paracetamol detected.

---

# 5. Education Agent

## Purpose

Generate patient-friendly explanations.

## Responsibilities

- Translate instructions
- Simplify medical terminology
- Support multiple languages

Supported Languages

- English
- Kannada
- Hindi

---

# 6. Reminder Agent

*Status: Planned, not yet implemented in the current build.*

## Purpose

Help patients follow treatment.

## Responsibilities

- Generate medication schedule
- Daily reminders
- Missed dose tracking

Example

8:00 AM

✔ Paracetamol

2:00 PM

✔ Vitamin Tablet

8:00 PM

✔ Antibiotic

---

# Agent Communication

Each agent receives structured output from the previous agent.

Vision Agent

↓

Verification Agent

↓

Medication Intelligence Agent

↓

Safety Agent

↓

Education Agent

↓

Reminder Agent

This modular architecture makes CuraLens AI easier to maintain, extend, and improve.

---

# Future Agents

Future versions may include:

- Voice Assistant Agent
- Caregiver Agent
- Hospital Integration Agent
- Analytics Agent
- Follow-up Agent

These are outside the MVP scope.