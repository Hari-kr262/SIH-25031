"""Notifications screen."""
import flet as ft
from frontend.themes.colors import AppColors


def _notification_item(notif: dict) -> ft.Container:
    """Build a single notification list item."""
    type_icons = {
        "issue_update": ft.Icons.UPDATE,
        "issue_resolved": ft.Icons.CHECK_CIRCLE_OUTLINED,
        "comment": ft.Icons.COMMENT_OUTLINED,
        "vote": ft.Icons.THUMB_UP_OUTLINED,
        "badge": ft.Icons.EMOJI_EVENTS_OUTLINED,
        "system": ft.Icons.INFO_OUTLINED,
    }
    icon = type_icons.get(notif.get("type", "system"), ft.Icons.NOTIFICATIONS_OUTLINED)
    is_read = notif.get("is_read", False)
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(icon, color=AppColors.PRIMARY, size=24),
                    bgcolor=AppColors.SURFACE,
                    border_radius=24,
                    padding=10,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            notif.get("title", "Notification"),
                            size=14,
                            weight=ft.FontWeight.W_600 if not is_read else ft.FontWeight.NORMAL,
                            color=AppColors.DARK,
                        ),
                        ft.Text(
                            notif.get("message", ""),
                            size=12,
                            color=AppColors.GREY,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Text(
                            notif.get("time", ""),
                            size=11,
                            color=AppColors.GREY,
                            italic=True,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.Container(
                    width=8, height=8,
                    bgcolor=AppColors.PRIMARY if not is_read else ft.Colors.TRANSPARENT,
                    border_radius=4,
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor=AppColors.CARD_BG if not is_read else AppColors.BACKGROUND,
        border=ft.border.only(bottom=ft.BorderSide(1, AppColors.DIVIDER)),
    )


class NotificationsPage:
    """Citizen notifications list."""

    def __init__(self, page: ft.Page, **kwargs):
        self.page = page
        self._notifications = []
        self._list_view = ft.Column(controls=[], spacing=0, expand=True)

    def build(self) -> ft.View:
        self._load_notifications()
        return ft.View(
            route="/citizen/notifications",
            controls=[
                ft.AppBar(
                    title=ft.Text("Notifications", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                    leading=ft.IconButton(
                        ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.page.go("/citizen/home"),
                        icon_color=AppColors.ON_PRIMARY,
                    ),
                    actions=[
                        ft.TextButton(
                            "Mark all read",
                            on_click=self._mark_all_read,
                            style=ft.ButtonStyle(color=AppColors.ON_PRIMARY),
                        ),
                    ],
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[self._list_view],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    expand=True,
                ),
            ],
        )

    def _load_notifications(self):
        """Load notifications from API."""
        try:
            import httpx
            from config.settings import settings
            token = self.page.session_data.get("access_token")
            resp = httpx.get(
                f"{settings.API_BASE_URL}/api/v1/notifications/",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            if resp.status_code == 200:
                self._notifications = resp.json().get("notifications", [])
        except Exception:
            self._notifications = []
        self._refresh_list()

    def _refresh_list(self):
        """Rebuild the notification list."""
        if not self._notifications:
            self._list_view.controls = [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.NOTIFICATIONS_NONE, size=64, color=AppColors.GREY),
                            ft.Text("No notifications yet", size=16, color=AppColors.GREY),
                            ft.Text(
                                "You'll be notified when your issues are updated",
                                size=13, color=AppColors.GREY,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    expand=True,
                    padding=40,
                    alignment=ft.Alignment(0, 0),
                )
            ]
        else:
            self._list_view.controls = [
                _notification_item(n) for n in self._notifications
            ]

    def _mark_all_read(self, e):
        """Mark all notifications as read and persist to API."""
        try:
            import httpx
            from config.settings import settings
            token = self.page.session_data.get("access_token")
            httpx.post(
                f"{settings.API_BASE_URL}/api/v1/notifications/mark-all-read",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
        except Exception:
            pass
        for n in self._notifications:
            n["is_read"] = True
        self._refresh_list()
        self.page.update()
