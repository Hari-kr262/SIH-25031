"""Citizen home/dashboard screen."""
import flet as ft
from frontend.themes.colors import AppColors
from frontend.components.stat_card import StatCard
from frontend.components.issue_card import IssueCard
from frontend.components.empty_state import EmptyState
from frontend.components.loading_spinner import LoadingSpinner


_NAV_ITEMS = [
    {"icon": ft.Icons.HOME_OUTLINED, "selected_icon": ft.Icons.HOME, "label": "Home"},
    {"icon": ft.Icons.LIST_ALT_OUTLINED, "selected_icon": ft.Icons.LIST_ALT, "label": "My Issues"},
    {"icon": ft.Icons.ADD_CIRCLE_OUTLINE, "selected_icon": ft.Icons.ADD_CIRCLE, "label": "Report"},
    {"icon": ft.Icons.LEADERBOARD_OUTLINED, "selected_icon": ft.Icons.LEADERBOARD, "label": "Leaders"},
    {"icon": ft.Icons.PERSON_OUTLINE, "selected_icon": ft.Icons.PERSON, "label": "Profile"},
]

_NAV_ROUTES = [
    "/citizen/home",
    "/citizen/issues",
    "/citizen/report",
    "/citizen/leaderboard",
    "/citizen/profile",
]


class CitizenHome:
    """Citizen home dashboard."""

    def __init__(self, page: ft.Page, on_report_issue, on_view_issue):
        self.page = page
        self.on_report_issue = on_report_issue
        self.on_view_issue = on_view_issue
        self.issues = []
        self.stats = {}
        self.content = ft.Column(controls=[LoadingSpinner()])

    def build(self) -> ft.View:
        self._load_data()
        resolved_count = sum(1 for i in self.issues if i.get("status") == "resolved")
        unread_count = self._get_unread_notification_count()

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

        notif_icon = ft.Stack(
            controls=[
                ft.IconButton(
                    ft.Icons.NOTIFICATIONS_OUTLINED,
                    icon_color=AppColors.ON_PRIMARY,
                    on_click=lambda e: self.page.go("/citizen/notifications"),
                    tooltip="Notifications",
                ),
                *(
                    [ft.Container(
                        content=ft.Text(
                            str(unread_count) if unread_count < 10 else "9+",
                            size=9,
                            color=AppColors.ON_PRIMARY,
                            weight=ft.FontWeight.BOLD,
                        ),
                        bgcolor=AppColors.ERROR,
                        border_radius=8,
                        padding=ft.padding.symmetric(horizontal=4, vertical=1),
                        right=4,
                        top=4,
                    )]
                    if unread_count > 0 else []
                ),
            ],
        )

        return ft.View(
            route="/citizen/home",
            controls=[
                ft.AppBar(
                    title=ft.Text("CivicResolve", color=AppColors.ON_PRIMARY,
                                 weight=ft.FontWeight.BOLD),
                    bgcolor=AppColors.PRIMARY,
                    actions=[notif_icon],
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            # Welcome card
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(
                                        f"Hello, {self.page.session.get('full_name') or 'Citizen'}! 👋",
                                        size=20, weight=ft.FontWeight.BOLD,
                                        color=AppColors.ON_PRIMARY,
                                    ),
                                    ft.Text("Report civic issues in your area",
                                           color=ft.Colors.WHITE70, size=13),
                                ], spacing=4),
                                bgcolor=AppColors.PRIMARY,
                                padding=20,
                                border_radius=ft.border_radius.only(
                                    bottom_left=20, bottom_right=20
                                ),
                            ),
                            ft.Container(height=8),
                            # Stats row
                            ft.Row(
                                controls=[
                                    StatCard("My Reports", str(len(self.issues)), "report", AppColors.PRIMARY),
                                    StatCard("Resolved", str(resolved_count), "check_circle", AppColors.SUCCESS),
                                ],
                                scroll=ft.ScrollMode.AUTO,
                            ),
                            ft.Container(height=8),
                            # Quick action
                            ft.Container(
                                content=ft.ElevatedButton(
                                    "🚨 Report a New Issue",
                                    on_click=self.on_report_issue,
                                    bgcolor=AppColors.PRIMARY,
                                    color=AppColors.ON_PRIMARY,
                                    width=float("inf"),
                                    height=50,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=12)
                                    ),
                                ),
                                padding=ft.padding.symmetric(horizontal=4),
                            ),
                            ft.Container(height=8),
                            ft.Text("Recent Issues", size=16, weight=ft.FontWeight.BOLD),
                            self.content,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        spacing=8,
                    ),
                    padding=16,
                    expand=True,
                ),
            ],
            bottom_appbar=ft.BottomAppBar(content=nav_bar, padding=ft.padding.all(0)),
        )

    def _load_data(self):
        """Load issues from API."""
        try:
            import httpx
            from config.settings import settings
            token = self.page.session.get("access_token")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            resp = httpx.get(
                f"{settings.API_BASE_URL}/api/v1/issues/my",
                headers=headers,
                timeout=5,
            )
            if resp.status_code == 200:
                data = resp.json()
                self.issues = data.get("data", {}).get("items", [])
                if self.issues:
                    self.content.controls = [
                        IssueCard(issue, on_tap=lambda e, i=issue: self.on_view_issue(i))
                        for issue in self.issues[:5]
                    ]
                else:
                    self.content.controls = [
                        EmptyState(
                            icon="report_problem",
                            title="No issues yet",
                            subtitle="Be the first to report a civic issue in your area",
                            action_text="Report Issue",
                            on_action=self.on_report_issue,
                        )
                    ]
        except Exception:
            self.content.controls = [
                EmptyState(icon="wifi_off", title="Could not load issues",
                           subtitle="Check your connection and try again")
            ]

    def _get_unread_notification_count(self) -> int:
        """Fetch unread notification count from API."""
        try:
            import httpx
            from config.settings import settings
            token = self.page.session.get("access_token")
            if not token:
                return 0
            resp = httpx.get(
                f"{settings.API_BASE_URL}/api/v1/notifications/unread-count",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5,
            )
            if resp.status_code == 200:
                return resp.json().get("count", 0)
        except Exception:
            pass
        return 0
