from fastapi import Depends
from app.services.aadhar_verification_service import AadharVerificationService

def get_aadhar_service() -> AadharVerificationService:
    """Provider for AadharVerificationService."""
    return AadharVerificationService()
