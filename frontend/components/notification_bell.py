"""Notification bell icon with unread count badge."""
import flet as ft
from frontend.themes.colors import AppColors


def NotificationBell(unread_count: int = 0, on_click=None) -> ft.Stack:
    """Bell icon with badge for unread notification count."""
    controls = [
        ft.IconButton(icon="notifications", on_click=on_click, icon_color=AppColors.ON_PRIMARY),
    ]
    if unread_count > 0:
        controls.append(
            ft.Container(
                content=ft.Text(
                    str(min(unread_count, 99)),
                    size=9,
                    color=ft.colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
                bgcolor=AppColors.ERROR,
                border_radius=10,
                padding=ft.padding.symmetric(horizontal=5, vertical=2),
                right=4,
                top=4,
            )
        )
    return ft.Stack(controls=controls, width=48, height=48)
