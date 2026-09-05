# API Reference - Phishing Detection System

## Base URL
http://localhost:5000

## Web UI Endpoints

### GET /
Main dashboard interface
- Returns: HTML page with statistics and prediction form
- Status: 200 OK

### POST /predict
Form-based URL prediction
- Form Data: 
  - url (required): string
- Returns: HTML page with result
- Status: 200 OK

---

## REST API Endpoints (JSON)

### 1. POST /api/predict
Predict if a URL is phishing

**Request:**
`json
{
  "url": "https://example.com"
}
`

**Success Response (200):**
`json
{
  "success": true,
  "url": "https://example.com",
  "result": "Legit",
  "is_phishing": false,
  "confidence": 95.5,
  "timestamp": "2026-04-06 14:30:00"
}
`

**Error Response (400/500):**
`json
{
  "success": false,
  "error": "Error message here",
  "status_code": 400
}
`

---

### 2. GET /api/statistics
Get overall detection statistics

**Response (200):**
`json
{
  "success": true,
  "statistics": {
    "phishing": 10,
    "legit": 25,
    "total": 35,
    "phishing_percentage": 28.57
  }
}
`

---

### 3. GET /api/history
Get detection history

**Query Parameters:**
- limit (optional): integer, default=50

**Example:** GET /api/history?limit=10

**Response (200):**
`json
{
  "success": true,
  "total": 35,
  "history": [
    {
      "url": "https://example.com",
      "result": "Legit",
      "confidence": 95.5,
      "time": "2026-04-06 14:30:00"
    },
    ...
  ]
}
`

---

### 4. POST /api/clear-history
Clear all detection history

**Request:** 
Empty POST request

**Response (200):**
`json
{
  "success": true,
  "message": "History cleared"
}
`

---

## Result Values

- **result**: "Legit" or "Phishing"
- **is_phishing**: boolean (true if phishing, false if legitimate)
- **confidence**: float (0-100), probability score

## Status Codes

- 200: Success
- 400: Bad request (invalid URL)
- 500: Server error (model not loaded)

## Example cURL Commands

### Predict URL
\\\ash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
\\\

### Get Statistics
\\\ash
curl http://localhost:5000/api/statistics
\\\

### Get Last 20 Records
\\\ash
curl "http://localhost:5000/api/history?limit=20"
\\\

### Clear History
\\\ash
curl -X POST http://localhost:5000/api/clear-history
\\\

## Python Example

\\\python
import requests
import json

# Predict URL
response = requests.post(
    'http://localhost:5000/api/predict',
    json={'url': 'https://example.com'},
    headers={'Content-Type': 'application/json'}
)

data = response.json()
print(f"Result: {data['result']}")
print(f"Confidence: {data['confidence']}%")
print(f"Is Phishing: {data['is_phishing']}")
\\\

## JavaScript Example

\\\javascript
// Predict URL
fetch('http://localhost:5000/api/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({'url': 'https://example.com'})
})
.then(response => response.json())
.then(data => {
    console.log('Result:', data.result);
    console.log('Confidence:', data.confidence);
    console.log('Is Phishing:', data.is_phishing);
});
\\\

---

**Last Updated:** April 6, 2026
