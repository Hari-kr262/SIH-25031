"""Landing page — public-facing welcome screen."'''
import flet as ft
from frontend.themes.colors import AppColors


class LandingPage:
    """CivicResolve public landing page."'''

    def __init__(self, page: ft.Page, on_login, on_register):
        self.page = page
        self.on_login = on_login
        self.on_register = on_register

    def build(self) -> ft.View:
        return ft.View(
            route="/",
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=60),
                            ft.Text("🏛️", size=80, text_align=ft.TextAlign.CENTER),
                            ft.Text(
                                "CivicResolve",
                                size=36,
                                weight=ft.FontWeight.BOLD,
                                color=AppColors.ON_PRIMARY,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "Crowdsourced Civic Issue Reporting\n& Resolution System",
                                size=14,
                                color=ft.Colors.WHITE70,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "Smart India Hackathon 2025 | Jharkhand",
                                size=11,
                                color=ft.Colors.WHITE54,
                                text_align=ft.TextAlign.CENTER,
                                italic=True,
                            ),
                            ft.Container(height=40),
                            ft.ElevatedButton(
                                "Get Started — Report Issues",
                                on_click=self.on_register,
                                bgcolor=AppColors.ON_PRIMARY,
                                color=AppColors.PRIMARY,
                                width=280,
                                height=50,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
                            ),
                            ft.TextButton(
                                "Already have an account? Login",
                                on_click=self.on_login,
                                style=ft.ButtonStyle(color=ft.Colors.WHITE),
                            ),
                            ft.Container(height=40),
                            # Stats row
                            ft.Row(
                                controls=[
                                    self._stat("🕳️", "Potholes"),
                                    self._stat("🗑️", "Garbage"),
                                    self._stat("💡", "Streetlights"),
                                    self._stat("💧", "Leaks"),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=16,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(0, -1),
                        end=ft.Alignment(0, 1),
                        colors=[AppColors.PRIMARY, AppColors.PRIMARY_DARK],
                    ),
                    expand=True,
                    padding=ft.padding.symmetric(horizontal=30),
                )
            ],
            bgcolor=AppColors.PRIMARY,
        )

    def _stat(self, icon: str, label: str) -> ft.Column:
        return ft.Column(
            controls=[ft.Text(icon, size=30), ft.Text(label, size=10, color=ft.Colors.WHITE70)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        )
