"""Admin analytics screen."""
import flet as ft
from frontend.themes.colors import AppColors


def _bar(label: str, value: int, max_value: int, color: str) -> ft.Container:
    """Build a simple horizontal progress bar for a metric."""
    pct = (value / max_value) if max_value > 0 else 0
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(label, size=12, color=AppColors.DARK, expand=True),
                        ft.Text(str(value), size=12, weight=ft.FontWeight.BOLD, color=color),
                    ],
                ),
                ft.Container(
                    content=ft.Container(
                        bgcolor=color,
                        border_radius=4,
                        width=None,
                        expand=pct,
                    ),
                    bgcolor=AppColors.DIVIDER,
                    border_radius=4,
                    height=10,
                    expand=True,
                ),
            ],
            spacing=4,
        ),
        padding=ft.padding.symmetric(vertical=6),
    )


class AdminAnalyticsPage:
    """Admin analytics — trends, performance, and SLA data."""

    def __init__(self, page: ft.Page):
        self.page = page
        self._trends = {}
        self._performance = {}
        self._sla = {}

    def build(self) -> ft.View:
        self._load_data()

        # Trends section
        trend_controls = [ft.Text("📈 Issue Trends (Last 30 Days)",
                                  size=16, weight=ft.FontWeight.BOLD)]
        if self._trends:
            daily = self._trends.get("daily_counts", [])
            total = sum(d.get("count", 0) for d in daily) if daily else self._trends.get("total", 0)
            trend_controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                self._stat_row("Total Issues", str(total), AppColors.PRIMARY),
                                self._stat_row("Resolved",
                                               str(self._trends.get("resolved", 0)), AppColors.SUCCESS),
                                self._stat_row("Avg. Resolution Time",
                                               f"{self._trends.get('avg_resolution_hours', 0):.1f} hrs",
                                               AppColors.INFO),
                            ],
                            spacing=8,
                        ),
                        padding=16,
                    ),
                )
            )
        else:
            trend_controls.append(ft.Text("No trend data available.", size=13, color=AppColors.GREY))

        # Performance section
        perf_controls = [ft.Text("🏆 Department Performance",
                                 size=16, weight=ft.FontWeight.BOLD)]
        depts = (
            self._performance if isinstance(self._performance, list)
            else self._performance.get("departments", [])
        )
        if depts:
            max_issues = max((d.get("issues_count", 0) for d in depts), default=1)
            for dept in depts[:10]:
                perf_controls.append(
                    _bar(
                        dept.get("name", "Unknown"),
                        dept.get("issues_count", 0),
                        max_issues,
                        AppColors.PRIMARY,
                    )
                )
        else:
            perf_controls.append(ft.Text("No performance data.", size=13, color=AppColors.GREY))

        # SLA section
        sla_controls = [ft.Text("⏱️ SLA Compliance", size=16, weight=ft.FontWeight.BOLD)]
        if self._sla:
            sla_controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                self._stat_row("Total Issues",
                                               str(self._sla.get("total_issues", 0)), AppColors.PRIMARY),
                                self._stat_row("SLA Met",
                                               str(self._sla.get("sla_met", 0)), AppColors.SUCCESS),
                                self._stat_row("SLA Breached",
                                               str(self._sla.get("sla_breached", 0)), AppColors.ERROR),
                                self._stat_row("Compliance Rate",
                                               f"{self._sla.get('compliance_rate', 0):.1f}%",
                                               AppColors.INFO),
                            ],
                            spacing=8,
                        ),
                        padding=16,
                    ),
                )
            )
        else:
            sla_controls.append(ft.Text("No SLA data available.", size=13, color=AppColors.GREY))

        return ft.View(
            route="/admin/analytics",
            controls=[
                ft.AppBar(
                    title=ft.Text("Analytics", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                    leading=ft.IconButton(
                        ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.page.go("/admin/dashboard"),
                        icon_color=AppColors.ON_PRIMARY,
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            *trend_controls,
                            ft.Container(height=8),
                            *perf_controls,
                            ft.Container(height=8),
                            *sla_controls,
                        ],
                        spacing=8,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=16,
                    expand=True,
                ),
            ],
        )

    def _load_data(self):
        """Load analytics data from API."""
        try:
            import httpx
            from config.settings import settings
            token = self.page.client_storage.get("access_token")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            base = settings.API_BASE_URL

            r1 = httpx.get(f"{base}/api/v1/analytics/trends?days=30", headers=headers, timeout=10)
            if r1.status_code == 200:
                self._trends = r1.json()

            r2 = httpx.get(f"{base}/api/v1/analytics/performance", headers=headers, timeout=10)
            if r2.status_code == 200:
                self._performance = r2.json()

            r3 = httpx.get(f"{base}/api/v1/analytics/sla", headers=headers, timeout=10)
            if r3.status_code == 200:
                self._sla = r3.json()
        except Exception:
            pass

    def _stat_row(self, label: str, value: str, color: str) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Text(label, size=13, color=AppColors.GREY, expand=True),
                ft.Text(value, size=14, weight=ft.FontWeight.BOLD, color=color),
            ],
        )
