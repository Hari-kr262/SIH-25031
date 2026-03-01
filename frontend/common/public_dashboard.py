"""Public dashboard screen — city-wide stats and recent issues (no auth required)."""
import flet as ft
from frontend.themes.colors import AppColors
from frontend.common import api_client
from frontend.components.stat_card import StatCard
from frontend.components.loading_spinner import LoadingSpinner
from frontend.components.empty_state import EmptyState


_CATEGORY_EMOJI = {
    "pothole": "🕳️",
    "garbage": "🗑️",
    "streetlight": "💡",
    "water_leak": "💧",
    "drainage": "🌊",
    "road_damage": "🛣️",
    "illegal_dumping": "🚮",
    "fallen_tree": "🌳",
    "sewage": "💩",
    "public_property": "🏛️",
    "other": "📋",
}

_STATUS_COLOR = {
    "pending": AppColors.PENDING,
    "in_progress": AppColors.IN_PROGRESS,
    "resolved": AppColors.RESOLVED,
    "closed": AppColors.CLOSED,
}


class PublicDashboardPage:
    """Publicly accessible city issues dashboard."""

    def __init__(self, page: ft.Page, **kwargs):
        self.page = page
        self._stats = {}
        self._issues = []
        self._stats_row = ft.Row(
            controls=[LoadingSpinner()],
            wrap=True,
            spacing=12,
            run_spacing=12,
        )
        self._issue_list = ft.Column(
            controls=[LoadingSpinner()],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=4,
        )

    def build(self) -> ft.View:
        """Build and return the Public Dashboard view."""
        self._load_data()
        return ft.View(
            route="/public/dashboard",
            controls=[
                ft.AppBar(
                    title=ft.Text("Public Dashboard", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "📊 City-Wide Issue Statistics",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=AppColors.TEXT_PRIMARY,
                            ),
                            self._stats_row,
                            ft.Divider(height=1, color=AppColors.DIVIDER),
                            ft.Text(
                                "🕐 Recent Public Issues",
                                size=15,
                                weight=ft.FontWeight.W_600,
                                color=AppColors.TEXT_PRIMARY,
                            ),
                            ft.Container(
                                content=self._issue_list,
                                expand=True,
                            ),
                            ft.Divider(height=1, color=AppColors.DIVIDER),
                            ft.ElevatedButton(
                                "🔑 Login to Report an Issue",
                                on_click=lambda e: self.page.go("/login"),
                                bgcolor=AppColors.PRIMARY,
                                color=AppColors.ON_PRIMARY,
                                width=280,
                            ),
                        ],
                        expand=True,
                        spacing=12,
                    ),
                    expand=True,
                    padding=16,
                ),
            ],
        )

    def _load_data(self):
        """Fetch stats and recent issues from the API."""
        # Try the public dashboard endpoint first, fall back to issues list
        try:
            stats_data = api_client.get("/dashboard/public")
            if isinstance(stats_data, dict) and stats_data:
                self._stats = stats_data
            else:
                self._stats = {}
        except Exception:
            self._stats = {}

        # Fetch recent issues (public, no auth)
        try:
            issues_data = api_client.get("/issues?page=1&page_size=10")
            if isinstance(issues_data, list):
                self._issues = issues_data
            elif isinstance(issues_data, dict):
                self._issues = issues_data.get("issues", issues_data.get("results", []))
            else:
                self._issues = []
        except Exception:
            self._issues = []

        # If stats endpoint was empty, show zeros rather than misleading partial counts
        if not self._stats:
            self._stats = {
                "total": 0,
                "resolved": 0,
                "in_progress": 0,
                "pending": 0,
            }

        self._render_stats()
        self._render_issues()

    def _render_stats(self):
        """Populate the stats card row."""
        s = self._stats
        total = str(s.get("total", s.get("total_issues", 0)))
        resolved = str(s.get("resolved", s.get("resolved_issues", 0)))
        in_progress = str(s.get("in_progress", s.get("in_progress_issues", 0)))
        pending = str(s.get("pending", s.get("pending_issues", 0)))

        self._stats_row.controls = [
            StatCard("Total Reported", total, icon="report_problem", color=AppColors.INFO),
            StatCard("Resolved", resolved, icon="check_circle", color=AppColors.SUCCESS),
            StatCard("In Progress", in_progress, icon="autorenew", color=AppColors.IN_PROGRESS),
            StatCard("Pending", pending, icon="hourglass_empty", color=AppColors.PENDING),
        ]

    def _render_issues(self):
        """Populate the recent issues list."""
        if not self._issues:
            self._issue_list.controls = [
                EmptyState(
                    icon=ft.Icons.INBOX_OUTLINED,
                    title="No issues yet",
                    subtitle="Be the first to report a civic issue!",
                )
            ]
            return

        rows = []
        for issue in self._issues:
            category = issue.get("category", "other")
            emoji = _CATEGORY_EMOJI.get(category, "📋")
            status = issue.get("status", "pending")
            status_color = _STATUS_COLOR.get(status, AppColors.GREY)
            rows.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(emoji, size=20),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            issue.get("title", "Untitled"),
                                            size=13,
                                            weight=ft.FontWeight.W_600,
                                            color=AppColors.TEXT_PRIMARY,
                                        ),
                                        ft.Text(
                                            issue.get("address") or issue.get("ward") or "—",
                                            size=11,
                                            color=AppColors.GREY,
                                        ),
                                    ],
                                    expand=True,
                                    spacing=2,
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        status.replace("_", " ").title(),
                                        size=10,
                                        color=AppColors.ON_PRIMARY,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    bgcolor=status_color,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=12,
                                ),
                            ],
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=12, vertical=10),
                    ),
                    elevation=1,
                    margin=ft.margin.only(bottom=4),
                )
            )
        self._issue_list.controls = rows
