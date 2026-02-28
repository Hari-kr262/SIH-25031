"""
Smart router — automatically routes issues to the correct department.
Uses category-to-department mapping and geographic assignment.
"""

from typing import Optional, Dict


CATEGORY_DEPT_MAP = {
    "pothole": "Roads & Infrastructure",
    "road_damage": "Roads & Infrastructure",
    "streetlight": "Electricity",
    "water_leak": "Water & Sanitation",
    "sewage": "Water & Sanitation",
    "garbage": "Solid Waste Management",
    "illegal_dumping": "Solid Waste Management",
    "drainage": "Drainage",
    "fallen_tree": "Parks & Recreation",
    "public_property": "Public Property",
    "other": "Public Property",
}


class SmartRouter:
    """Routes civic issues to the appropriate department."""

    def route(self, category: str, ward: Optional[str] = None) -> Dict:
        """
        Determine the correct department for an issue.
        Returns dict with department_name and routing_confidence.
        """
        dept_name = CATEGORY_DEPT_MAP.get(category, "Public Property")
        confidence = 0.95 if category in CATEGORY_DEPT_MAP else 0.5

        return {
            "department_name": dept_name,
            "routing_confidence": confidence,
            "routing_reason": f"Category '{category}' mapped to {dept_name}",
        }

    def route_with_db(self, category: str, db) -> Optional[int]:
        """Route and return the department_id from the database."""
        routing = self.route(category)
        from backend.models.department import Department
        dept = db.query(Department).filter_by(
            name=routing["department_name"], is_active=True
        ).first()
        return dept.id if dept else None


smart_router = SmartRouter()
