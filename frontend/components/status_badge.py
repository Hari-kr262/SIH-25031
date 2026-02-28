"""Status badge component for issue status display."""
import flet as ft


STATUS_COLORS = {
    "pending":      ("#FF8F00", "#FFFFFF"),
    "verified":     ("#1565C0", "#FFFFFF"),
    "assigned":     ("#6A1B9A", "#FFFFFF"),
    "in_progress":  ("#0277BD", "#FFFFFF"),
    "fix_uploaded": ("#00695C", "#FFFFFF"),
    "resolved":     ("#2E7D32", "#FFFFFF"),
    "rejected":     ("#C62828", "#FFFFFF"),
    "escalated":    ("#BF360C", "#FFFFFF"),
    "closed":       ("#424242", "#FFFFFF"),
}


def StatusBadge(status: str) -> ft.Container:
    """Create a colored status badge."""
    bg, fg = STATUS_COLORS.get(status, ("#9E9E9E", "#FFFFFF"))
    return ft.Container(
        content=ft.Text(status.replace("_", " ").title(), size=11, color=fg,
                        weight=ft.FontWeight.W_500),
        bgcolor=bg,
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=10, vertical=4),
    )
