# Aadhar Service - Quick Reference

## Valid Aadhar Numbers (For Testing)

```
123456789012
234567890123
345678901234
456789012345
567890123456
678901234567
789012345678
890123456789
901234567890
012345678901
```

## Quick Start

### 1. Start Aadhar Service
```bash
cd "c:\Users\DELL\Downloads\BT Project\BT-ECO-SYSTEM\GDB\gdb-service\aadhar_service"
uvicorn app.main:app --reload --port 8005
```

### 2. Start Accounts Service
```bash
cd "c:\Users\DELL\Downloads\BT Project\BT-ECO-SYSTEM\GDB\gdb-service\accounts_service"
uvicorn app.main:app --reload --port 8002
```

### 3. Update Database (First Time Only)
```bash
cd "c:\Users\DELL\Downloads\BT Project\BT-ECO-SYSTEM\GDB\gdb-service\accounts_service"
python setup_db.py
```

## API Endpoints

### Aadhar Service (Port 8005)
- **Health:** `GET http://localhost:8005/health`
- **Verify:** `POST http://localhost:8005/api/v1/verify`
- **Valid Numbers:** `GET http://localhost:8005/api/v1/valid-numbers`
- **Docs:** http://localhost:8005/docs

### Accounts Service (Port 8002)
- **Create Savings:** `POST http://localhost:8002/api/v1/accounts/savings`
- **Docs:** http://localhost:8002/api/v1/docs

## Test Request

### Create Savings Account with Valid Aadhar
```json
POST http://localhost:8002/api/v1/accounts/savings

{
  "name": "John Doe",
  "pin": "1234",
  "date_of_birth": "1990-01-01",
  "gender": "Male",
  "phone_no": "9876543210",
  "aadhar_number": "123456789012",
  "privilege": "SILVER"
}
```

### Expected Success Response
```json
{
  "account_number": 1000,
  "message": "Savings account created successfully"
}
```

### Test Invalid Aadhar (Should Fail)
```json
{
  "name": "Jane Doe",
  "pin": "5678",
  "date_of_birth": "1995-05-15",
  "gender": "Female",
  "phone_no": "9876543211",
  "aadhar_number": "999999999999",
  "privilege": "GOLD"
}
```

### Expected Error Response
```json
{
  "error_code": "VALIDATION_ERROR",
  "message": "Aadhar verification failed: Aadhar number not found in UIDAI database"
}
```

## Architecture

```
User Request (Savings Account)
    ↓
Accounts Service (Port 8002)
    ↓ (HTTP Call)
Aadhar Service (Port 8005)
    ↓ (Verify against 10 valid numbers)
Return: Valid/Invalid
    ↓
Accounts Service: Create or Reject
```

## Files Changed

### New Service
- `aadhar_service/` - Complete new microservice

### Accounts Service Updates
- `app/models/account.py` - Added aadhar_number field
- `app/database/accounts_schema.sql` - Added aadhar_number column
- `app/repositories/account_repo.py` - Updated INSERT
- `app/services/savings_impl.py` - Added verification call
- `app/utils/aadhar_client.py` - NEW HTTP client

## Troubleshooting

### Aadhar Service Not Running
**Error:** `Aadhar verification service is unavailable (connection refused)`

**Solution:** Start Aadhar service on port 8005

### Invalid Aadhar Number
**Error:** `Aadhar verification failed: Aadhar number not found in UIDAI database`

**Solution:** Use one of the 10 valid Aadhar numbers listed above

### Database Error
**Error:** `column "aadhar_number" does not exist`

**Solution:** Run `python setup_db.py` to update database schema
