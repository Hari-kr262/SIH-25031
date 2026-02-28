"""City map screen — stub implementation."""
import flet as ft
from frontend.themes.colors import AppColors


class CityMapPage:
    """Interactive city map showing reported issues."""

    def __init__(self, page: ft.Page, **kwargs):
        self.page = page

    def build(self) -> ft.View:
        return ft.View(
            route="/citizen/map",
            controls=[
                ft.AppBar(title=ft.Text("City Map", color=AppColors.ON_PRIMARY),
                         bgcolor=AppColors.PRIMARY),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("🗺️ City Map", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text("Coming soon...", color=AppColors.GREY),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    expand=True,
                    padding=20,
                )
            ],
        )
