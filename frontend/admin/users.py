"""Admin users management screen."""
import flet as ft
from frontend.themes.colors import AppColors


class AdminUsersPage:
    """List and manage all platform users."""

    def __init__(self, page: ft.Page):
        self.page = page
        self._all_users = []
        self._search_query = ""
        self._list_col = ft.Column(controls=[], spacing=8, expand=True)

    def build(self) -> ft.View:
        self._search_field = ft.TextField(
            hint_text="Search by name or email…",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=12,
            on_change=self._on_search,
            expand=True,
        )
        self._load_users()
        return ft.View(
            route="/admin/users",
            controls=[
                ft.AppBar(
                    title=ft.Text("Manage Users", color=AppColors.ON_PRIMARY),
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
                            ft.Row(controls=[self._search_field], spacing=8),
                            ft.Container(height=4),
                            ft.Container(
                                content=self._list_col,
                                expand=True,
                            ),
                        ],
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        spacing=8,
                    ),
                    padding=16,
                    expand=True,
                ),
            ],
        )

    def _load_users(self):
        """Fetch all users from API."""
        try:
            import httpx
            from config.settings import settings
            token = self.page.client_storage.get("access_token")
            resp = httpx.get(
                f"{settings.API_BASE_URL}/api/v1/admin/users",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                self._all_users = data if isinstance(data, list) else data.get("users", [])
        except Exception:
            self._all_users = []
        self._refresh_list()

    def _on_search(self, e):
        """Filter list on search input."""
        self._search_query = e.control.value.lower()
        self._refresh_list()
        self.page.update()

    def _refresh_list(self):
        """Re-render filtered user list."""
        query = self._search_query
        users = [
            u for u in self._all_users
            if not query or query in (u.get("full_name") or "").lower()
            or query in (u.get("email") or "").lower()
        ]

        if not users:
            self._list_col.controls = [
                ft.Container(
                    content=ft.Text("No users found.", size=14, color=AppColors.GREY),
                    alignment=ft.alignment.center,
                    padding=40,
                )
            ]
            return

        self._list_col.controls = [self._user_card(u) for u in users]

    def _user_card(self, user: dict) -> ft.Card:
        is_active = user.get("is_active", True)
        role = user.get("role", "citizen")
        role_colors = {
            "super_admin": AppColors.ERROR,
            "municipal_admin": AppColors.PRIMARY,
            "department_head": AppColors.INFO,
            "citizen": AppColors.SUCCESS,
        }
        role_color = role_colors.get(role, AppColors.GREY)

        toggle = ft.Switch(
            value=is_active,
            active_color=AppColors.SUCCESS,
            on_change=lambda e, uid=user.get("id"): self._toggle_active(uid, e.control.value),
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                (user.get("full_name") or "?")[:2].upper(),
                                size=14, weight=ft.FontWeight.BOLD,
                                color=AppColors.ON_PRIMARY,
                            ),
                            bgcolor=role_color,
                            border_radius=20,
                            width=40,
                            height=40,
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(user.get("full_name", "Unknown"), size=14,
                                        weight=ft.FontWeight.W_600, color=AppColors.DARK),
                                ft.Text(user.get("email", ""), size=12, color=AppColors.GREY),
                                ft.Container(
                                    content=ft.Text(role.replace("_", " ").title(),
                                                    size=10, color=AppColors.ON_PRIMARY),
                                    bgcolor=role_color,
                                    border_radius=8,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        toggle,
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
            ),
            elevation=1,
        )

    def _toggle_active(self, user_id, new_value: bool):
        """Toggle user active status via API."""
        try:
            import httpx
            from config.settings import settings
            token = self.page.client_storage.get("access_token")
            httpx.put(
                f"{settings.API_BASE_URL}/api/v1/admin/users/{user_id}/toggle-active",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
        except Exception:
            pass
