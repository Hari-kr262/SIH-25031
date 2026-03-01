"""Field worker home screen."""
import flet as ft
from frontend.themes.colors import AppColors
from frontend.components.issue_card import IssueCard
from frontend.components.empty_state import EmptyState


class WorkerHome:
    """Field worker dashboard showing assigned issues."""

    def __init__(self, page: ft.Page, on_view_issue):
        self.page = page
        self.on_view_issue = on_view_issue
        self.assigned_issues = []

    def build(self) -> ft.View:
        self._load_assigned()
        return ft.View(
            route="/worker/home",
            controls=[
                ft.AppBar(
                    title=ft.Text("My Assignments", color=AppColors.ON_PRIMARY,
                                 weight=ft.FontWeight.BOLD),
                    bgcolor=AppColors.PRIMARY,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                f"Hello, {self.page.session_data.get('full_name') or 'Worker'}! 🔧",
                                size=18, weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(f"{len(self.assigned_issues)} issue(s) assigned to you",
                                   size=13, color=AppColors.GREY),
                            ft.Container(height=8),
                            *([IssueCard(i, on_tap=lambda e, issue=i: self.on_view_issue(issue))
                               for i in self.assigned_issues]
                              if self.assigned_issues else
                              [EmptyState(icon="check_circle", title="All clear!",
                                         subtitle="No issues currently assigned to you")]),
                        ],
                        spacing=8,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=16,
                    expand=True,
                )
            ],
        )

    def _load_assigned(self):
        try:
            import httpx
            from config.settings import settings
            token = self.page.session_data.get("access_token")
            resp = httpx.get(
                f"{settings.API_BASE_URL}/api/v1/issues/my",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5,
            )
            if resp.status_code == 200:
                self.assigned_issues = resp.json().get("data", {}).get("items", [])
        except Exception:
            pass
