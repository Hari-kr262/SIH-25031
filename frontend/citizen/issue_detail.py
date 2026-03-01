"""Issue detail screen."""
import flet as ft
from frontend.themes.colors import AppColors
from frontend.components.status_badge import StatusBadge


CATEGORY_ICONS = {
    "pothole": "🕳️", "garbage": "🗑️", "streetlight": "💡",
    "water_leak": "💧", "drainage": "🌊", "road_damage": "🛣️",
    "illegal_dumping": "🚮", "fallen_tree": "🌳", "sewage": "💩",
    "public_property": "🏛️", "other": "📋",
}


class IssueDetailPage:
    """Detailed view for a single civic issue."""

    def __init__(self, page: ft.Page, issue_id: str = None, **kwargs):
        self.page = page
        self.issue_id = issue_id
        self._issue = {}

    def build(self) -> ft.View:
        self._load_issue()
        issue = self._issue
        icon = CATEGORY_ICONS.get(issue.get("category", "other"), "📋")
        title = issue.get("title", "Issue Detail")
        description = issue.get("description", "")
        address = issue.get("address") or issue.get("ward") or "Location not specified"
        category = issue.get("category", "other").replace("_", " ").title()
        priority = issue.get("priority", "medium").title()
        upvotes = issue.get("upvotes", 0)
        status = issue.get("status", "pending")

        return ft.View(
            route=f"/citizen/issue/{self.issue_id}",
            controls=[
                ft.AppBar(
                    title=ft.Text("Issue Detail", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                    leading=ft.IconButton(
                        ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.page.go("/citizen/issues"),
                        icon_color=AppColors.ON_PRIMARY,
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=8),
                            ft.Row(
                                controls=[
                                    ft.Text(f"{icon}", size=40),
                                    ft.Column(
                                        controls=[
                                            ft.Text(title, size=18, weight=ft.FontWeight.BOLD,
                                                    color=AppColors.DARK),
                                            StatusBadge(status),
                                        ],
                                        spacing=6,
                                        expand=True,
                                    ),
                                ],
                                spacing=16,
                                vertical_alignment=ft.CrossAxisAlignment.START,
                            ),
                            ft.Divider(color=AppColors.DIVIDER),
                            self._detail_row(ft.Icons.LOCATION_ON_OUTLINED, "Location", address),
                            self._detail_row(ft.Icons.CATEGORY_OUTLINED, "Category", category),
                            self._detail_row(ft.Icons.FLAG_OUTLINED, "Priority", priority),
                            self._detail_row(ft.Icons.THUMB_UP_OUTLINED, "Upvotes", str(upvotes)),
                            ft.Divider(color=AppColors.DIVIDER),
                            ft.Text("Description", size=14, weight=ft.FontWeight.W_600,
                                    color=AppColors.DARK),
                            ft.Text(
                                description or "No description provided.",
                                size=14,
                                color=AppColors.GREY if not description else AppColors.DARK,
                            ),
                            ft.Container(height=16),
                            ft.ElevatedButton(
                                "👍 Upvote this Issue",
                                on_click=self._handle_upvote,
                                bgcolor=AppColors.PRIMARY,
                                color=AppColors.ON_PRIMARY,
                                width=float("inf"),
                                height=48,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        spacing=12,
                    ),
                    padding=20,
                    expand=True,
                ),
            ],
        )

    def _load_issue(self):
        """Load issue data from API."""
        if not self.issue_id:
            return
        try:
            import httpx
            from config.settings import settings
            token = self.page.client_storage.get("access_token")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            resp = httpx.get(
                f"{settings.API_BASE_URL}/api/v1/issues/{self.issue_id}",
                headers=headers,
                timeout=10,
            )
            if resp.status_code == 200:
                self._issue = resp.json()
        except Exception:
            self._issue = {}

    def _handle_upvote(self, e):
        """Submit upvote for this issue and update UI."""
        if not self.issue_id:
            return
        btn = e.control
        try:
            import httpx
            from config.settings import settings
            token = self.page.client_storage.get("access_token")
            resp = httpx.post(
                f"{settings.API_BASE_URL}/api/v1/issues/{self.issue_id}/vote",
                headers={"Authorization": f"Bearer {token}"},
                json={"vote_type": "upvote"},
                timeout=10,
            )
            if resp.status_code in (200, 201):
                new_count = resp.json().get("upvotes", self._issue.get("upvotes", 0) + 1)
                self._issue["upvotes"] = new_count
                btn.text = f"👍 Upvoted ({new_count})"
                btn.disabled = True
            else:
                btn.text = "⚠️ Could not upvote. Try again."
        except Exception:
            btn.text = "⚠️ Connection error. Try again."
        self.page.update()

    def _detail_row(self, icon, label: str, value: str) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Icon(icon, size=18, color=AppColors.PRIMARY),
                ft.Text(f"{label}:", size=13, color=AppColors.GREY, width=80),
                ft.Text(value, size=13, color=AppColors.DARK, expand=True),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
