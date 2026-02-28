"""
CivicResolve - Main Application Entry Point
SIH 25031: Crowdsourced Civic Issue Reporting & Resolution System
Government of Jharkhand | Clean & Green Technology Theme
"""

import uvicorn
from backend.app import create_app
from config.settings import settings

app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
