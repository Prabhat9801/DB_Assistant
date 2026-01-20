"""
Health Check Routes
====================
API endpoints for monitoring service health.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import os

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    database: str
    llm: str
    version: str = "1.0.0"


@router.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check():
    """
    Check the health status of all services.
    
    Returns:
        HealthResponse with status of each component
    """
    from src.services.db_service import db_service
    
    # Check database connection
    try:
        db_status = "healthy" if db_service.test_connection() else "unhealthy"
    except Exception:
        db_status = "unhealthy"
    
    # Check LLM configuration
    llm_status = "healthy" if os.getenv("OPENAI_API_KEY") else "not_configured"
    
    # Overall status
    overall_status = "healthy" if db_status == "healthy" and llm_status == "healthy" else "degraded"
    
    return HealthResponse(
        status=overall_status,
        database=db_status,
        llm=llm_status
    )


@router.get("/ready", summary="Readiness check")
async def readiness_check():
    """
    Check if the service is ready to accept requests.
    """
    return {"ready": True}


@router.get("/live", summary="Liveness check")
async def liveness_check():
    """
    Check if the service is alive.
    """
    return {"alive": True}