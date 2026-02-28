"""Priority badge component."""
import flet as ft

PRIORITY_COLORS = {
    "critical": ("#B71C1C", "#FFFFFF"),
    "high":     ("#E53935", "#FFFFFF"),
    "medium":   ("#FB8C00", "#FFFFFF"),
    "low":      ("#43A047", "#FFFFFF"),
}


def PriorityBadge(priority: str) -> ft.Container:
    """Create a priority level badge."""
    bg, fg = PRIORITY_COLORS.get(priority, ("#9E9E9E", "#FFFFFF"))
    return ft.Container(
        content=ft.Text(priority.title(), size=11, color=fg, weight=ft.FontWeight.W_500),
        bgcolor=bg,
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=8, vertical=3),
    )
