"""Loading spinner component."""
import flet as ft
from frontend.themes.colors import AppColors


def LoadingSpinner(message: str = "Loading...") -> ft.Column:
    """Full-screen loading indicator."""
    return ft.Column(
        controls=[
            ft.ProgressRing(color=AppColors.PRIMARY, width=40, height=40),
            ft.Text(message, color=AppColors.GREY, size=14),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )
