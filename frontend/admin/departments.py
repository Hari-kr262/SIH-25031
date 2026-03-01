"""Admin departments management screen."""
import flet as ft
from frontend.themes.colors import AppColors


class AdminDepartmentsPage:
    """List and create departments."""

    def __init__(self, page: ft.Page):
        self.page = page
        self._departments = []
        self._list_col = ft.Column(controls=[], spacing=8)
        self._name_field = ft.TextField(label="Department Name", border_radius=12)
        self._desc_field = ft.TextField(label="Description", border_radius=12, multiline=True, min_lines=2)
        self._form_status = ft.Text("", color=AppColors.SUCCESS, size=13)
        self._form_error = ft.Text("", color=AppColors.ERROR, size=13)

    def build(self) -> ft.View:
        self._load_departments()
        return ft.View(
            route="/admin/departments",
            controls=[
                ft.AppBar(
                    title=ft.Text("Departments", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                    leading=ft.IconButton(
                        ft.icons.ARROW_BACK,
                        on_click=lambda e: self.page.go("/admin/dashboard"),
                        icon_color=AppColors.ON_PRIMARY,
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            # Create new department form
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text("➕ New Department", size=15,
                                                    weight=ft.FontWeight.W_600),
                                            self._name_field,
                                            self._desc_field,
                                            self._form_error,
                                            self._form_status,
                                            ft.ElevatedButton(
                                                "Create Department",
                                                on_click=self._create_department,
                                                bgcolor=AppColors.PRIMARY,
                                                color=AppColors.ON_PRIMARY,
                                                width=float("inf"),
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=10)
                                                ),
                                            ),
                                        ],
                                        spacing=10,
                                    ),
                                    padding=16,
                                ),
                                elevation=2,
                            ),
                            ft.Container(height=8),
                            ft.Text("Existing Departments", size=15, weight=ft.FontWeight.W_600),
                            self._list_col,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        spacing=8,
                    ),
                    padding=16,
                    expand=True,
                ),
            ],
        )

    def _load_departments(self):
        """Load departments from API."""
        try:
            import httpx
            from config.settings import settings
            token = self.page.client_storage.get("access_token")
            resp = httpx.get(
                f"{settings.API_BASE_URL}/api/v1/admin/departments",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                self._departments = data if isinstance(data, list) else data.get("departments", [])
        except Exception:
            self._departments = []
        self._refresh_list()

    def _refresh_list(self):
        """Re-render department list."""
        if not self._departments:
            self._list_col.controls = [
                ft.Text("No departments yet.", size=13, color=AppColors.GREY)
            ]
            return
        self._list_col.controls = [self._dept_card(d) for d in self._departments]

    def _dept_card(self, dept: dict) -> ft.Card:
        is_active = dept.get("is_active", True)
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.BUSINESS, color=AppColors.PRIMARY, size=28),
                        ft.Column(
                            controls=[
                                ft.Text(dept.get("name", ""), size=14,
                                        weight=ft.FontWeight.W_600, color=AppColors.DARK),
                                ft.Text(dept.get("description", ""), size=12,
                                        color=AppColors.GREY, max_lines=2,
                                        overflow=ft.TextOverflow.ELLIPSIS),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Active" if is_active else "Inactive",
                                size=11,
                                color=AppColors.ON_PRIMARY,
                            ),
                            bgcolor=AppColors.SUCCESS if is_active else AppColors.GREY,
                            border_radius=8,
                            padding=ft.padding.symmetric(horizontal=8, vertical=3),
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=16, vertical=14),
            ),
            elevation=1,
        )

    def _create_department(self, e):
        """Submit new department to API."""
        name = self._name_field.value.strip()
        desc = self._desc_field.value.strip()
        if not name:
            self._form_error.value = "Department name is required"
            self._form_status.value = ""
            self.page.update()
            return
        try:
            import httpx
            from config.settings import settings
            token = self.page.client_storage.get("access_token")
            resp = httpx.post(
                f"{settings.API_BASE_URL}/api/v1/admin/departments",
                json={"name": name, "description": desc},
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            if resp.status_code in (200, 201):
                self._form_status.value = "✅ Department created!"
                self._form_error.value = ""
                self._name_field.value = ""
                self._desc_field.value = ""
                self._load_departments()
            else:
                self._form_error.value = resp.json().get("detail", "Failed to create department")
                self._form_status.value = ""
        except Exception as ex:
            self._form_error.value = f"Error: {ex}"
            self._form_status.value = ""
        self.page.update()
