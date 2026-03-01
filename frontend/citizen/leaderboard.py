"""Leaderboard screen."""
import flet as ft
from frontend.themes.colors import AppColors


_MEDAL_COLORS = ["#FFD700", "#C0C0C0", "#CD7F32"]  # gold, silver, bronze


def _leaderboard_item(rank: int, entry: dict) -> ft.Container:
    """Build a single leaderboard row."""
    medal = _MEDAL_COLORS[rank - 1] if rank <= 3 else None
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        f"#{rank}" if rank > 3 else ["🥇", "🥈", "🥉"][rank - 1],
                        size=16 if rank > 3 else 22,
                        weight=ft.FontWeight.BOLD,
                        color=medal or AppColors.GREY,
                    ),
                    width=44,
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(
                    content=ft.Text(
                        (entry.get("full_name") or "User")[:2].upper(),
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.ON_PRIMARY,
                    ),
                    bgcolor=medal or AppColors.PRIMARY,
                    border_radius=20,
                    width=40,
                    height=40,
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            entry.get("full_name", "Anonymous"),
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=AppColors.DARK,
                        ),
                        ft.Text(
                            f"{entry.get('issues_count', 0)} issues reported",
                            size=12,
                            color=AppColors.GREY,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            str(entry.get("points", 0)),
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=AppColors.PRIMARY,
                        ),
                        ft.Text("pts", size=11, color=AppColors.GREY),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    spacing=0,
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor=AppColors.CARD_BG if rank <= 3 else AppColors.BACKGROUND,
        border=ft.border.only(bottom=ft.BorderSide(1, AppColors.DIVIDER)),
    )


class LeaderboardPage:
    """Community leaderboard showing top contributors."""

    def __init__(self, page: ft.Page, **kwargs):
        self.page = page
        self._entries = []
        self._list_col = ft.Column(controls=[], spacing=0, expand=True)

    def build(self) -> ft.View:
        self._load_leaderboard()
        return ft.View(
            route="/citizen/leaderboard",
            controls=[
                ft.AppBar(
                    title=ft.Text("Leaderboard", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                    leading=ft.IconButton(
                        ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.page.go("/citizen/home"),
                        icon_color=AppColors.ON_PRIMARY,
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    "🏆 Top Contributors",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                padding=ft.padding.symmetric(vertical=12),
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Container(
                                content=self._list_col,
                                expand=True,
                            ),
                        ],
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    expand=True,
                ),
            ],
        )

    def _load_leaderboard(self):
        """Load leaderboard data from API."""
        try:
            import httpx
            from config.settings import settings
            token = self.page.session.get("access_token")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            resp = httpx.get(
                f"{settings.API_BASE_URL}/api/v1/gamification/leaderboard",
                headers=headers,
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                self._entries = data if isinstance(data, list) else data.get("leaderboard", [])
        except Exception:
            self._entries = []
        self._refresh_list()

    def _refresh_list(self):
        """Rebuild leaderboard list."""
        if not self._entries:
            self._list_col.controls = [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.EMOJI_EVENTS_OUTLINED, size=64, color=AppColors.GREY),
                            ft.Text("No data available yet", size=16, color=AppColors.GREY),
                            ft.Text(
                                "Report issues to earn points and appear here!",
                                size=13, color=AppColors.GREY,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    padding=40,
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                )
            ]
        else:
            self._list_col.controls = [
                _leaderboard_item(i + 1, entry) for i, entry in enumerate(self._entries)
            ]
