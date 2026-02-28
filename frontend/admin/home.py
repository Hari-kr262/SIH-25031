"""Municipal admin home/dashboard screen."""
import flet as ft
from frontend.themes.colors import AppColors
from frontend.components.stat_card import StatCard
from frontend.components.loading_spinner import LoadingSpinner


class AdminHome:
    """Municipal admin dashboard."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.stats = {}

    def build(self) -> ft.View:
        self._load_stats()
        total = self.stats.get("total_issues", 0)
        resolved = self.stats.get("resolved_issues", 0)
        pending = self.stats.get("pending_issues", 0)
        users = self.stats.get("total_users", 0)

        return ft.View(
            route="/admin/home",
            controls=[
                ft.AppBar(
                    title=ft.Text("Admin Dashboard", color=AppColors.ON_PRIMARY,
                                 weight=ft.FontWeight.BOLD),
                    bgcolor=AppColors.PRIMARY,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("📊 Overview", size=18, weight=ft.FontWeight.BOLD),
                            ft.Container(height=8),
                            ft.Row(
                                controls=[
                                    StatCard("Total Issues", str(total), "report_problem", AppColors.PRIMARY),
                                    StatCard("Resolved", str(resolved), "check_circle", AppColors.SUCCESS),
                                ],
                                scroll=ft.ScrollMode.AUTO,
                            ),
                            ft.Row(
                                controls=[
                                    StatCard("Pending", str(pending), "hourglass_empty", AppColors.WARNING),
                                    StatCard("Total Users", str(users), "people", AppColors.INFO),
                                ],
                                scroll=ft.ScrollMode.AUTO,
                            ),
                            ft.Container(height=16),
                            ft.Text("Quick Actions", size=16, weight=ft.FontWeight.BOLD),
                            self._action_button("📋 All Issues", lambda e: self.page.go("/admin/issues"), AppColors.PRIMARY),
                            self._action_button("👥 Manage Users", lambda e: self.page.go("/admin/users"), AppColors.INFO),
                            self._action_button("📊 Analytics", lambda e: self.page.go("/admin/analytics"), AppColors.SUCCESS),
                            self._action_button("💰 Budget", lambda e: self.page.go("/admin/budget"), AppColors.WARNING),
                        ],
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=16,
                    expand=True,
                )
            ],
        )

    def _load_stats(self):
        try:
            import httpx
            from config.settings import settings
            token = self.page.client_storage.get("access_token")
            resp = httpx.get(
                f"{settings.API_BASE_URL}/api/v1/dashboard/admin",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5,
            )
            if resp.status_code == 200:
                self.stats = resp.json().get("data", {})
        except Exception:
            pass

    def _action_button(self, text: str, on_click, color: str) -> ft.Container:
        return ft.Container(
            content=ft.ElevatedButton(
                text, on_click=on_click, bgcolor=color,
                color=AppColors.ON_PRIMARY, width=float("inf"), height=48,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            ),
            padding=ft.padding.symmetric(horizontal=4),
        )
