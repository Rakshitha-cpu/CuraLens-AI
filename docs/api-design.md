# API Design

## Overview

CuraLens AI exposes RESTful APIs built with FastAPI.

Base URL

```
http://localhost:8000/api/v1
```

---

# Authentication

> Authentication will be added in a later phase using Firebase Authentication.

---

# 1. Health Check

### GET

```
/health
```

### Response

```json
{
  "status": "healthy",
  "service": "CuraLens AI API"
}
```

---

# 2. Upload Prescription

### POST

```
/prescriptions/upload
```

### Request

Multipart Form Data

| Field | Type |
|-------|------|
| image | File |

### Response

```json
{
  "prescriptionId":"P001",
  "status":"Uploaded"
}
```

---

# 3. Process Prescription

Triggers the AI Agent workflow.

### POST

```
/prescriptions/{prescriptionId}/process
```

### Response

```json
{
    "status":"Processing Started"
}
```

---

# 4. Get Prescription

### GET

```
/prescriptions/{prescriptionId}
```

### Response

```json
{
  "prescriptionId":"P001",
  "processingStatus":"Completed"
}
```

---

# 5. Get Medicines

### GET

```
/prescriptions/{prescriptionId}/medicines
```

### Response

```json
[
 {
   "medicineName":"Paracetamol",
   "dosage":"650 mg",
   "frequency":"Twice Daily",
   "duration":"5 Days"
 }
]
```

---

# 6. Verify Medicine

Used when the Verification Agent detects low confidence.

### POST

```
/medicines/{medicineId}/verify
```

### Request

```json
{
  "selectedMedicine":"Metformin"
}
```

### Response

```json
{
  "status":"Verified"
}
```

---

# 7. Medication Explanation

### GET

```
/medicines/{medicineId}/explanation
```

### Response

```json
{
  "purpose":"Treats bacterial infection",
  "timing":"After Food",
  "duration":"5 Days"
}
```

---

# 8. Generate Medication Schedule

### POST

```
/schedule/generate/{prescriptionId}
```

### Response

```json
{
 "scheduleCreated":true
}
```

---

# 9. Get Patient Schedule

### GET

```
/users/{userId}/schedule
```

### Response

```json
[
 {
   "medicine":"Paracetamol",
   "time":"08:00 AM",
   "status":"Pending"
 }
]
```

---

# 10. Update Reminder Status

### PATCH

```
/reminders/{reminderId}
```

### Request

```json
{
 "status":"Taken"
}
```

### Response

```json
{
 "updated":true
}
```

---

# 11. Get AI Agent Logs (Admin)

### GET

```
/logs/{prescriptionId}
```

Returns outputs from:

- Vision Agent
- Verification Agent
- Medication Intelligence Agent
- Safety Agent
- Education Agent
- Reminder Agent

---

# API Flow

```
Frontend

↓

Upload Prescription

↓

Backend

↓

Vision Agent

↓

Verification Agent

↓

Medication Agent

↓

Safety Agent

↓

Education Agent

↓

Reminder Agent

↓

Database

↓

Frontend
```

---

# HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

# Future APIs

- User Authentication
- Doctor Dashboard
- Caregiver Portal
- Voice Assistant
- Notification Settings
- Hospital Integration