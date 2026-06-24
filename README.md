# Aadhar Verification Service

Third-party API service for validating Aadhar numbers during Savings Account creation in the GDB Banking System.

## Overview

This service simulates the **UIDAI (Unique Identification Authority of India)** Aadhar verification system. It provides a REST API endpoint to verify whether an Aadhar number is valid.

## Purpose

- **Validates Aadhar numbers** during Savings Account creation
- **Separation of concerns** - Account service doesn't need to know validation logic
- **Independent deployment** - Can be updated without touching Account Service
- **Realistic simulation** - Mimics real UIDAI verification flow

## Architecture

```
Savings Account Creation Request
    ↓
Account Service validates basic data
    ↓
Calls Aadhar Service API (HTTP)
    ↓
Aadhar Service checks against hardcoded valid numbers
    ↓
Returns verification response (True/False)
    ↓
Account Service proceeds or rejects
```

## Valid Aadhar Numbers

For testing purposes, the following 10 Aadhar numbers are considered valid:

1. `123456789012`
2. `234567890123`
3. `345678901234`
4. `456789012345`
5. `567890123456`
6. `678901234567`
7. `789012345678`
8. `890123456789`
9. `901234567890`
10. `012345678901`

**Any other Aadhar number will be rejected as invalid.**

## API Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "service": "aadhar_service",
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Verify Aadhar Number
```http
POST /api/v1/verify
Content-Type: application/json

{
  "aadhar_number": "123456789012"
}
```

**Success Response (Valid Aadhar):**
```json
{
  "aadhar_number": "123456789012",
  "is_valid": true,
  "status": "VERIFIED",
  "message": "Aadhar number verified successfully",
  "timestamp": "2026-01-21T00:00:00Z"
}
```

**Failure Response (Invalid Aadhar):**
```json
{
  "aadhar_number": "999999999999",
  "is_valid": false,
  "status": "INVALID",
  "message": "Aadhar number not found in UIDAI database",
  "timestamp": "2026-01-21T00:00:00Z"
}
```

### 3. Get Valid Numbers (Testing)
```http
GET /api/v1/valid-numbers
```

**Response:**
```json
{
  "valid_aadhar_numbers": [
    "012345678901",
    "123456789012",
    ...
  ],
  "count": 10
}
```

## Installation

1. **Navigate to service directory:**
   ```bash
   cd aadhar_service
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Service

### Development Mode
```bash
uvicorn app.main:app --reload --port 8005
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8005
```

### Using Python directly
```bash
python -m app.main
```

The service will start on **http://localhost:8005**

## API Documentation

Once the service is running, access the interactive API documentation:

- **Swagger UI:** http://localhost:8005/docs
- **ReDoc:** http://localhost:8005/redoc

## Testing

### Using cURL
```bash
# Valid Aadhar
curl -X POST http://localhost:8005/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"aadhar_number": "123456789012"}'

# Invalid Aadhar
curl -X POST http://localhost:8005/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"aadhar_number": "999999999999"}'
```

### Using Python
```python
import requests

response = requests.post(
    "http://localhost:8005/api/v1/verify",
    json={"aadhar_number": "123456789012"}
)
print(response.json())
```

## Configuration

Environment variables can be set in `.env` file:

```env
SERVICE_NAME=aadhar_service
PORT=8005
HOST=0.0.0.0
LOG_LEVEL=INFO
API_V1_PREFIX=/api/v1
```

## Integration with Accounts Service

The Accounts Service will call this API during Savings Account creation:

1. User submits savings account creation request with Aadhar number
2. Accounts Service validates basic data
3. Accounts Service calls `POST /api/v1/verify` with Aadhar number
4. If `is_valid: true`, account creation proceeds
5. If `is_valid: false`, account creation is rejected with error

## Error Handling

- **400 Bad Request:** Invalid Aadhar format (not 12 digits, contains non-numeric characters)
- **500 Internal Server Error:** Unexpected server error

## Logging

The service logs all verification attempts with masked Aadhar numbers for privacy:
```
2026-01-21 00:00:00 - INFO - Verifying Aadhar number: 1234********
2026-01-21 00:00:00 - INFO - ✅ Aadhar verification successful: 1234********
```

## Security Notes

- In production, replace hardcoded numbers with actual UIDAI API integration
- Implement rate limiting to prevent abuse
- Add authentication/authorization for API access
- Use HTTPS for secure communication
- Implement proper logging and monitoring

## Author

GDB Architecture Team

## Version

1.0.0
