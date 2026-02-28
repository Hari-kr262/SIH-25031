"""Pydantic schemas for dashboard stats."""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel


class PublicStats(BaseModel):
    total_issues: int
    resolved_issues: int
    pending_issues: int
    in_progress_issues: int
    resolution_rate: float
    avg_resolution_hours: float
    issues_by_category: Dict[str, int]
    issues_by_status: Dict[str, int]
    top_wards: List[Dict[str, Any]]


class AdminStats(PublicStats):
    total_users: int
    active_citizens: int
    total_volunteers: int
    total_workers: int
    sla_breached: int
    sla_at_risk: int
    budget_utilized_percent: float
    issues_today: int
    issues_this_week: int
    fake_reports_detected: int


class DepartmentStats(BaseModel):
    department_id: int
    department_name: str
    total_issues: int
    pending: int
    in_progress: int
    resolved: int
    avg_resolution_hours: float
    sla_breached: int
    budget_allocated: float
    budget_spent: float
    worker_count: int
