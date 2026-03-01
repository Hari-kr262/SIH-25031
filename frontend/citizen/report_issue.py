"""Report issue screen for citizens."""
import flet as ft
from frontend.themes.colors import AppColors


CATEGORIES = [
    ("pothole", "🕳️ Pothole"),
    ("garbage", "🗑️ Garbage"),
    ("streetlight", "💡 Streetlight"),
    ("water_leak", "💧 Water Leak"),
    ("drainage", "🌊 Drainage"),
    ("road_damage", "🛣️ Road Damage"),
    ("illegal_dumping", "🚮 Illegal Dumping"),
    ("fallen_tree", "🌳 Fallen Tree"),
    ("sewage", "💩 Sewage"),
    ("public_property", "🏛️ Public Property"),
    ("other", "📋 Other"),
]

PRIORITIES = [("critical", "Critical"), ("high", "High"), ("medium", "Medium"), ("low", "Low")]


class ReportIssuePage:
    """Issue reporting form."""

    def __init__(self, page: ft.Page, on_submit_success):
        self.page = page
        self.on_submit_success = on_submit_success
        self.title_field = ft.TextField(label="Issue Title *", hint_text="e.g. Large pothole near bus stop",
                                        border_radius=12, max_length=200)
        self.desc_field = ft.TextField(label="Description", hint_text="Describe the issue in detail",
                                       multiline=True, min_lines=3, border_radius=12)
        self.address_field = ft.TextField(label="Address / Location", border_radius=12)
        self.ward_field = ft.TextField(label="Ward Number", border_radius=12)
        self.category_dd = ft.Dropdown(
            label="Category *",
            border_radius=12,
            options=[ft.dropdown.Option(k, v) for k, v in CATEGORIES],
            value="other",
        )
        self.priority_dd = ft.Dropdown(
            label="Priority",
            border_radius=12,
            options=[ft.dropdown.Option(k, v) for k, v in PRIORITIES],
            value="medium",
        )
        self.anonymous_checkbox = ft.Checkbox(label="Report Anonymously", value=False)
        self.status_text = ft.Text("", color=AppColors.SUCCESS)
        self.error_text = ft.Text("", color=AppColors.ERROR)

    def build(self) -> ft.View:
        return ft.View(
            route="/citizen/report",
            controls=[
                ft.AppBar(
                    title=ft.Text("Report Civic Issue", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                    leading=ft.IconButton("arrow_back", on_click=lambda e: self.page.go("/citizen/home"),
                                         icon_color=AppColors.ON_PRIMARY),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("📸 Report an Issue", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text("Help improve your city by reporting civic issues",
                                   size=13, color=AppColors.GREY),
                            ft.Container(height=8),
                            self.title_field,
                            self.desc_field,
                            self.category_dd,
                            self.priority_dd,
                            self.address_field,
                            self.ward_field,
                            self.anonymous_checkbox,
                            self.error_text,
                            self.status_text,
                            ft.Container(height=8),
                            ft.ElevatedButton(
                                "Submit Report",
                                on_click=self._submit,
                                bgcolor=AppColors.PRIMARY,
                                color=AppColors.ON_PRIMARY,
                                width=float("inf"),
                                height=50,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                            ),
                        ],
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=20,
                    expand=True,
                )
            ],
        )

    def _submit(self, e):
        """Submit issue to API."""
        title = self.title_field.value.strip()
        if not title:
            self.error_text.value = "Title is required"
            self.page.update()
            return

        try:
            import httpx
            from config.settings import settings
            token = self.page.session.get("access_token")
            resp = httpx.post(
                f"{settings.API_BASE_URL}/api/v1/issues/",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "title": title,
                    "description": self.desc_field.value,
                    "category": self.category_dd.value,
                    "priority": self.priority_dd.value,
                    "address": self.address_field.value,
                    "ward": self.ward_field.value,
                    "is_anonymous": self.anonymous_checkbox.value,
                },
                timeout=10,
            )
            if resp.status_code == 201:
                self.status_text.value = "✅ Issue submitted successfully!"
                self.error_text.value = ""
                self.page.update()
                import time
                time.sleep(1.5)
                self.on_submit_success()
            else:
                self.error_text.value = resp.json().get("detail", "Submission failed")
                self.page.update()
        except Exception as ex:
            self.error_text.value = f"Error: {ex}"
            self.page.update()
