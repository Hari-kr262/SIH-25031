"""Profile screen."""
import flet as ft
from frontend.themes.colors import AppColors


class ProfilePage:
    """Citizen profile and settings."""

    def __init__(self, page: ft.Page, **kwargs):
        self.page = page
        self._user = {}

    def build(self) -> ft.View:
        self._load_profile()
        name = self._user.get("full_name") or self.page.session_data.get("full_name") or "Citizen"
        email = self._user.get("email", "")
        points = self._user.get("points", 0)
        badges = self._user.get("badges", [])
        issues_count = self._user.get("issues_count", 0)
        resolved_count = self._user.get("resolved_count", 0)

        avatar_initials = "".join(w[0].upper() for w in name.split()[:2]) if name else "C"

        return ft.View(
            route="/citizen/profile",
            controls=[
                ft.AppBar(
                    title=ft.Text("Profile", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                    leading=ft.IconButton(
                        ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.page.go("/citizen/home"),
                        icon_color=AppColors.ON_PRIMARY,
                    ),
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
                            # Avatar + name header
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text(
                                                avatar_initials,
                                                size=32,
                                                weight=ft.FontWeight.BOLD,
                                                color=AppColors.ON_PRIMARY,
                                            ),
                                            bgcolor=AppColors.PRIMARY,
                                            border_radius=40,
                                            width=80,
                                            height=80,
                                            alignment=ft.Alignment(0, 0),
                                        ),
                                        ft.Text(name, size=20, weight=ft.FontWeight.BOLD),
                                        ft.Text(email, size=13, color=AppColors.GREY),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=8,
                                ),
                                padding=ft.padding.symmetric(vertical=24),
                                alignment=ft.Alignment(0, 0),
                            ),
                            # Stats row
                            ft.Row(
                                controls=[
                                    self._stat_item(str(points), "Points", ft.Icons.STAR_OUTLINED),
                                    ft.VerticalDivider(width=1, color=AppColors.DIVIDER),
                                    self._stat_item(str(issues_count), "Reported", ft.Icons.REPORT_OUTLINED),
                                    ft.VerticalDivider(width=1, color=AppColors.DIVIDER),
                                    self._stat_item(str(resolved_count), "Resolved", ft.Icons.CHECK_CIRCLE_OUTLINED),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            ),
                            ft.Divider(color=AppColors.DIVIDER),
                            # Badges section
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("🏅 Badges", size=16, weight=ft.FontWeight.W_600),
                                        ft.Container(height=4),
                                        ft.Row(
                                            controls=(
                                                [ft.Text(b, size=24) for b in badges[:6]]
                                                if badges
                                                else [ft.Text("No badges yet", size=13, color=AppColors.GREY)]
                                            ),
                                            wrap=True,
                                            spacing=8,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                                padding=ft.padding.symmetric(horizontal=4, vertical=8),
                            ),
                            ft.Divider(color=AppColors.DIVIDER),
                            # Settings items
                            self._settings_item(ft.Icons.NOTIFICATIONS_OUTLINED, "Notification Preferences",
                                                lambda e: None),
                            self._settings_item(ft.Icons.LOCK_OUTLINED, "Change Password",
                                                lambda e: self.page.go("/forgot-password")),
                            self._settings_item(ft.Icons.LANGUAGE_OUTLINED, "Language", lambda e: None),
                            self._settings_item(ft.Icons.HELP_OUTLINE, "Help & Support", lambda e: None),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                        spacing=0,
                    ),
                    expand=True,
                    padding=ft.padding.symmetric(horizontal=16),
                ),
            ],
        )

    def _load_profile(self):
        """Load profile from API."""
        try:
            import httpx
            from config.settings import settings
            token = self.page.session_data.get("access_token")
            resp = httpx.get(
                f"{settings.API_BASE_URL}/api/v1/users/me",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            if resp.status_code == 200:
                self._user = resp.json()
        except Exception:
            self._user = {}

    def _handle_logout(self, e):
        """Clear session and redirect to landing."""
        for key in ("access_token", "refresh_token", "user_id", "user_role", "full_name"):
            try:
                self.page.session_data.pop(key, None)
            except Exception:
                pass
        self.page.go("/")

    def _stat_item(self, value: str, label: str, icon) -> ft.Column:
        return ft.Column(
            controls=[
                ft.Icon(icon, color=AppColors.PRIMARY, size=22),
                ft.Text(value, size=18, weight=ft.FontWeight.BOLD, color=AppColors.DARK),
                ft.Text(label, size=11, color=AppColors.GREY),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        )

    def _settings_item(self, icon, label: str, on_click) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color=AppColors.PRIMARY, size=22),
                    ft.Text(label, size=14, expand=True),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=AppColors.GREY, size=18),
                ],
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=4, vertical=14),
            border=ft.border.only(bottom=ft.BorderSide(1, AppColors.DIVIDER)),
            on_click=on_click,
            ink=True,
        )
