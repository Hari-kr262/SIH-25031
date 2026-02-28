"""Standardized API response helpers."""

from typing import Any, Dict
from fastapi.responses import JSONResponse


def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> Dict:
    """Return a standardized success response."""
    return {"success": True, "message": message, "data": data}


def error_response(message: str, status_code: int = 400, details: Any = None) -> JSONResponse:
    """Return a standardized error response."""
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "message": message, "details": details},
    )


def paginated_response(items: list, total: int, page: int, page_size: int) -> Dict:
    """Return a standardized paginated response."""
    import math
    return {
        "success": True,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": math.ceil(total / page_size) if page_size > 0 else 0,
        },
    }
