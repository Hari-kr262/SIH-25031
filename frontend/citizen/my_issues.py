"""My issues screen."""
import flet as ft
from frontend.themes.colors import AppColors
from frontend.components.issue_card import IssueCard
from frontend.components.empty_state import EmptyState
from frontend.components.loading_spinner import LoadingSpinner


_STATUS_FILTERS = ["All", "Pending", "In Progress", "Resolved", "Rejected"]


class MyIssuesPage:
    """Citizen's submitted issues list with filtering."""

    def __init__(self, page: ft.Page, on_view_issue=None, **kwargs):
        self.page = page
        self.on_view_issue = on_view_issue or (lambda issue: None)
        self._all_issues = []
        self._selected_filter = "All"
        self._content = ft.Column(
            controls=[LoadingSpinner()],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def build(self) -> ft.View:
        self._filter_row = ft.Row(
            controls=[
                ft.FilterChip(
                    label=ft.Text(f),
                    selected=(f == self._selected_filter),
                    on_select=lambda e, name=f: self._apply_filter(name),
                    selected_color=AppColors.PRIMARY,
                )
                for f in _STATUS_FILTERS
            ],
            scroll=ft.ScrollMode.AUTO,
        )
        self._load_issues()
        return ft.View(
            route="/citizen/issues",
            controls=[
                ft.AppBar(
                    title=ft.Text("My Issues", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                    leading=ft.IconButton(
                        ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.page.go("/citizen/home"),
                        icon_color=AppColors.ON_PRIMARY,
                    ),
                    actions=[
                        ft.IconButton(
                            ft.Icons.ADD_CIRCLE_OUTLINE,
                            icon_color=AppColors.ON_PRIMARY,
                            tooltip="Report new issue",
                            on_click=lambda e: self.page.go("/citizen/report"),
                        ),
                    ],
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=self._filter_row,
                                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                            ),
                            ft.Divider(height=1, color=AppColors.DIVIDER),
                            ft.Container(
                                content=self._content,
                                expand=True,
                                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                            ),
                        ],
                        expand=True,
                    ),
                    expand=True,
                ),
            ],
        )

    def _load_issues(self):
        """Load citizen issues from API."""
        try:
            import httpx
            from config.settings import settings
            token = self.page.client_storage.get("access_token")
            resp = httpx.get(
                f"{settings.API_BASE_URL}/api/v1/issues/my",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                self._all_issues = data if isinstance(data, list) else data.get("issues", [])
        except Exception:
            self._all_issues = []
        self._refresh_list()

    def _apply_filter(self, filter_name: str):
        """Filter issues by status."""
        self._selected_filter = filter_name
        for chip in self._filter_row.controls:
            chip.selected = (chip.label.value == filter_name)
        self._refresh_list()
        self.page.update()

    def _refresh_list(self):
        """Re-render the issue list based on current filter."""
        status_map = {
            "All": None,
            "Pending": "pending",
            "In Progress": "in_progress",
            "Resolved": "resolved",
            "Rejected": "rejected",
        }
        status_filter = status_map.get(self._selected_filter)
        issues = (
            self._all_issues if status_filter is None
            else [i for i in self._all_issues if i.get("status") == status_filter]
        )
        if not issues:
            self._content.controls = [
                EmptyState(
                    icon=ft.Icons.INBOX_OUTLINED,
                    title="No issues found",
                    subtitle="Tap + to report a new civic issue",
                    action_text="Report Issue",
                    on_action=lambda e: self.page.go("/citizen/report"),
                )
            ]
        else:
            self._content.controls = [
                IssueCard(issue, on_tap=lambda e, i=issue: self.on_view_issue(i))
                for issue in issues
            ]
