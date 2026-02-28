"""OTP model — database-backed OTP storage."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from config.database import Base


class OTPRecord(Base):
    __tablename__ = "otp_records"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    otp_code = Column(String(10), nullable=False)
    purpose = Column(String(50), nullable=False, default="verification")
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
