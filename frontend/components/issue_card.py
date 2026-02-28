"""Issue card component for list display."""
import flet as ft
from frontend.themes.colors import AppColors
from frontend.components.status_badge import StatusBadge


CATEGORY_ICONS = {
    "pothole": "🕳️",
    "garbage": "🗑️",
    "streetlight": "💡",
    "water_leak": "💧",
    "drainage": "🌊",
    "road_damage": "🛣️",
    "illegal_dumping": "🚮",
    "fallen_tree": "🌳",
    "sewage": "💩",
    "public_property": "🏛️",
    "other": "📋",
}


def IssueCard(issue: dict, on_tap=None) -> ft.Card:
    """Create an issue summary card."""
    icon = CATEGORY_ICONS.get(issue.get("category", "other"), "📋")
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(f"{icon} {issue.get('title', 'Untitled')}", size=15,
                            weight=ft.FontWeight.W_600, expand=True),
                    StatusBadge(issue.get("status", "pending")),
                ]),
                ft.Text(
                    issue.get("address") or issue.get("ward") or "Location not specified",
                    size=12, color=AppColors.GREY,
                ),
                ft.Row([
                    ft.Icon("thumb_up", size=14, color=AppColors.PRIMARY),
                    ft.Text(str(issue.get("upvotes", 0)), size=12),
                    ft.Text("•", color=AppColors.GREY),
                    ft.Text(
                        issue.get("category", "other").replace("_", " ").title(),
                        size=12, color=AppColors.INFO,
                    ),
                ], spacing=6),
            ], spacing=6),
            padding=16,
            on_click=on_tap,
            ink=True,
        ),
        elevation=1,
        margin=ft.margin.only(bottom=8),
    )
