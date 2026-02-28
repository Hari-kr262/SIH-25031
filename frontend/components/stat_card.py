"""Reusable statistics card component."""
import flet as ft
from frontend.themes.colors import AppColors


def StatCard(title: str, value: str, icon: str = "bar_chart", color: str = AppColors.PRIMARY) -> ft.Card:
    """Create a statistics display card."""
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([
                        ft.Icon(icon, color=color, size=28),
                        ft.Text(title, size=13, color=AppColors.GREY, weight=ft.FontWeight.W_500),
                    ], spacing=8),
                    ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=AppColors.DARK),
                ],
                spacing=8,
            ),
            padding=20,
            width=200,
        ),
        elevation=2,
    )
