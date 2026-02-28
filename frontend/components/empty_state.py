"""Empty state component for when there's no data."""
import flet as ft
from frontend.themes.colors import AppColors


def EmptyState(
    icon: str = "inbox",
    title: str = "Nothing here yet",
    subtitle: str = "",
    action_text: str = "",
    on_action=None,
) -> ft.Column:
    """Display an empty state with optional CTA button."""
    controls = [
        ft.Icon(icon, size=64, color=AppColors.GREY),
        ft.Text(title, size=18, weight=ft.FontWeight.W_600, color=AppColors.DARK),
    ]
    if subtitle:
        controls.append(ft.Text(subtitle, size=14, color=AppColors.GREY, text_align=ft.TextAlign.CENTER))
    if action_text and on_action:
        controls.append(
            ft.ElevatedButton(action_text, on_click=on_action, bgcolor=AppColors.PRIMARY,
                              color=AppColors.ON_PRIMARY)
        )
    return ft.Column(
        controls=controls,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12,
    )
