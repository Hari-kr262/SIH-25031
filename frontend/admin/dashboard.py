"""Admin dashboard screen."""
import flet as ft
from frontend.themes.colors import AppColors
from frontend.components.stat_card import StatCard


_NAV_ITEMS = [
    {"icon": ft.Icons.DASHBOARD_OUTLINED, "selected_icon": ft.Icons.DASHBOARD, "label": "Dashboard"},
    {"icon": ft.Icons.PEOPLE_OUTLINE, "selected_icon": ft.Icons.PEOPLE, "label": "Users"},
    {"icon": ft.Icons.BUSINESS_OUTLINED, "selected_icon": ft.Icons.BUSINESS, "label": "Departments"},
    {"icon": ft.Icons.BAR_CHART_OUTLINED, "selected_icon": ft.Icons.BAR_CHART, "label": "Analytics"},
]

_NAV_ROUTES = [
    "/admin/dashboard",
    "/admin/users",
    "/admin/departments",
    "/admin/analytics",
]


class AdminDashboard:
    """Admin overview dashboard with stats and department performance."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.stats = {}
        self.departments = []

    def build(self) -> ft.View:
        self._load_stats()

        total = self.stats.get("total_issues", 0)
        resolved = self.stats.get("resolved_issues", 0)
        pending = self.stats.get("pending_issues", 0)
        users = self.stats.get("total_users", 0)
        sla_breached = self.stats.get("sla_breached", 0)

        def _on_nav_change(e):
            idx = e.control.selected_index
            if idx != 0:
                self.page.go(_NAV_ROUTES[idx])

        nav_bar = ft.NavigationBar(
            selected_index=0,
            on_change=_on_nav_change,
            bgcolor=AppColors.BACKGROUND,
            indicator_color=AppColors.PRIMARY,
            destinations=[
                ft.NavigationBarDestination(
                    icon=item["icon"],
                    selected_icon=item["selected_icon"],
                    label=item["label"],
                )
                for item in _NAV_ITEMS
            ],
        )

        dept_rows = []
        for dept in self.departments[:10]:
            dept_rows.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(dept.get("name", ""), size=13, expand=True, color=AppColors.DARK),
                            ft.Text(str(dept.get("issues_count", 0)), size=13, color=AppColors.PRIMARY, width=50),
                            ft.Text(str(dept.get("resolved_count", 0)), size=13, color=AppColors.SUCCESS, width=60),
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.symmetric(horizontal=4, vertical=10),
                    border=ft.border.only(bottom=ft.BorderSide(1, AppColors.DIVIDER)),
                )
            )

        dept_section = []
        if dept_rows:
            dept_section = [
                ft.Text("Department Performance", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Department", size=12, color=AppColors.GREY, expand=True),
                            ft.Text("Issues", size=12, color=AppColors.GREY, width=50),
                            ft.Text("Resolved", size=12, color=AppColors.GREY, width=60),
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.symmetric(horizontal=4, vertical=6),
                    bgcolor=AppColors.SURFACE,
                    border_radius=8,
                ),
                *dept_rows,
            ]

        return ft.View(
            route="/admin/dashboard",
            controls=[
                ft.AppBar(
                    title=ft.Text("Admin Dashboard", color=AppColors.ON_PRIMARY,
                                  weight=ft.FontWeight.BOLD),
                    bgcolor=AppColors.PRIMARY,
                    actions=[
                        ft.IconButton(
                            ft.Icons.LOGOUT,
                            icon_color=AppColors.ON_PRIMARY,
                            tooltip="Logout",
                            on_click=self._handle_logout,
                        ),
                    ],
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=4),
                            ft.Text("📊 Overview", size=18, weight=ft.FontWeight.BOLD),
                            ft.Container(height=4),
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
                            ft.Row(
                                controls=[
                                    StatCard("SLA Breached", str(sla_breached), "warning", AppColors.ERROR),
                                ],
                                scroll=ft.ScrollMode.AUTO,
                            ),
                            ft.Container(height=8),
                            *dept_section,
                        ],
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=16,
                    expand=True,
                ),
            ],
            bottom_appbar=ft.BottomAppBar(content=nav_bar, padding=ft.padding.all(0)),
        )

    def _load_stats(self):
        """Load admin dashboard stats from API."""
        try:
            import httpx
            from config.settings import settings
            token = self.page.client_storage.get("access_token")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            resp = httpx.get(
                f"{settings.API_BASE_URL}/api/v1/dashboard/admin",
                headers=headers,
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                self.stats = data.get("data", data)
                self.departments = self.stats.get("departments", [])
        except Exception:
            pass

    def _handle_logout(self, e):
        """Clear session and redirect to landing."""
        for key in ("access_token", "refresh_token", "user_id", "user_role", "full_name"):
            try:
                self.page.client_storage.remove(key)
            except Exception:
                pass
        self.page.go("/")
