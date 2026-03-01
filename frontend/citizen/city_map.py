"""City map screen — shows nearby civic issues with map link."""
import flet as ft
from frontend.themes.colors import AppColors
from frontend.common import api_client
from frontend.components.issue_card import IssueCard, CATEGORY_ICONS
from frontend.components.status_badge import StatusBadge
from frontend.components.loading_spinner import LoadingSpinner
from frontend.components.empty_state import EmptyState


_CATEGORY_FILTERS = ["All", "Pothole", "Garbage", "Streetlight", "Water Leak", "Drainage", "Other"]

_CATEGORY_MAP = {
    "All": None,
    "Pothole": "pothole",
    "Garbage": "garbage",
    "Streetlight": "streetlight",
    "Water Leak": "water_leak",
    "Drainage": "drainage",
    "Other": "other",
}


class CityMapPage:
    """Interactive city map showing reported issues."""

    def __init__(self, page: ft.Page, **kwargs):
        self.page = page
        self._all_issues = []
        self._selected_filter = "All"
        self._content = ft.Column(
            controls=[LoadingSpinner()],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def build(self) -> ft.View:
        """Build and return the City Map view."""
        self._filter_row = ft.Row(
            controls=[
                ft.FilterChip(
                    label=ft.Text(f),
                    selected=(f == self._selected_filter),
                    on_select=lambda e, name=f: self._apply_filter(name),
                    selected_color=AppColors.PRIMARY,
                )
                for f in _CATEGORY_FILTERS
            ],
            scroll=ft.ScrollMode.AUTO,
        )
        self._load_issues()
        return ft.View(
            route="/citizen/map",
            controls=[
                ft.AppBar(
                    title=ft.Text("City Map", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                    leading=ft.IconButton(
                        ft.icons.ARROW_BACK,
                        on_click=lambda e: self.page.go("/citizen/home"),
                        icon_color=AppColors.ON_PRIMARY,
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            # Map button section
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "🗺️ Civic Issues Map",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color=AppColors.TEXT_PRIMARY,
                                        ),
                                        ft.Text(
                                            "View issue locations around Jharkhand",
                                            size=12,
                                            color=AppColors.GREY,
                                        ),
                                        ft.ElevatedButton(
                                            "📍 Open in Google Maps",
                                            on_click=lambda e: self.page.launch_url(
                                                "https://maps.google.com/?q=23.3441,85.3096"
                                            ),
                                            bgcolor=AppColors.PRIMARY,
                                            color=AppColors.ON_PRIMARY,
                                            width=240,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=8,
                                ),
                                bgcolor=AppColors.CARD_BG,
                                padding=ft.padding.symmetric(vertical=16, horizontal=12),
                                border_radius=8,
                                border=ft.border.all(1, AppColors.DIVIDER),
                            ),
                            ft.Divider(height=1, color=AppColors.DIVIDER),
                            # Category filter chips
                            ft.Container(
                                content=self._filter_row,
                                padding=ft.padding.symmetric(vertical=4),
                            ),
                            ft.Divider(height=1, color=AppColors.DIVIDER),
                            # Issues list
                            ft.Container(
                                content=self._content,
                                expand=True,
                            ),
                        ],
                        expand=True,
                        spacing=8,
                    ),
                    expand=True,
                    padding=12,
                ),
            ],
        )

    def _load_issues(self):
        """Fetch issues from API and populate the list."""
        try:
            token = self.page.client_storage.get("access_token")
            data = api_client.get("/issues?page=1&page_size=20", token=token)
            if isinstance(data, list):
                self._all_issues = data
            elif isinstance(data, dict):
                self._all_issues = data.get("issues", data.get("results", []))
            else:
                self._all_issues = []
        except Exception:
            self._all_issues = []
        self._refresh_list()

    def _apply_filter(self, filter_name: str):
        """Filter issues by category."""
        self._selected_filter = filter_name
        for chip in self._filter_row.controls:
            chip.selected = (chip.label.value == filter_name)
        self._refresh_list()
        self.page.update()

    def _refresh_list(self):
        """Re-render the issue list based on current category filter."""
        category_filter = _CATEGORY_MAP.get(self._selected_filter)
        issues = (
            self._all_issues if category_filter is None
            else [i for i in self._all_issues if i.get("category") == category_filter]
        )
        if not issues:
            self._content.controls = [
                EmptyState(
                    icon=ft.icons.MAP_OUTLINED,
                    title="No issues found",
                    subtitle="No civic issues reported in this category yet",
                )
            ]
        else:
            self._content.controls = [
                IssueCard(issue) for issue in issues
            ]
