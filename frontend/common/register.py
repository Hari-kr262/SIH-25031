"""Registration screen."""
import flet as ft
from frontend.themes.colors import AppColors


class RegisterPage:
    """Citizen registration screen."""

    def __init__(self, page: ft.Page, on_register_success, on_go_login):
        self.page = page
        self.on_register_success = on_register_success
        self.on_go_login = on_go_login
        self.name_field = ft.TextField(label="Full Name", border_radius=12)
        self.email_field = ft.TextField(
            label="Email", keyboard_type=ft.KeyboardType.EMAIL, border_radius=12
        )
        self.phone_field = ft.TextField(
            label="Phone (optional)", keyboard_type=ft.KeyboardType.PHONE, border_radius=12
        )
        self.password_field = ft.TextField(
            label="Password", password=True, can_reveal_password=True, border_radius=12
        )
        self.error_text = ft.Text("", color=AppColors.ERROR, size=13)

    def build(self) -> ft.View:
        return ft.View(
            route="/register",
            controls=[
                ft.AppBar(
                    title=ft.Text("Create Account", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=10),
                            ft.Text("Join CivicResolve 🏛️", size=22, weight=ft.FontWeight.BOLD),
                            ft.Text("Help improve your city", size=14, color=AppColors.GREY),
                            ft.Container(height=16),
                            self.name_field,
                            self.email_field,
                            self.phone_field,
                            self.password_field,
                            self.error_text,
                            ft.Container(height=8),
                            ft.ElevatedButton(
                                "Create Account",
                                on_click=self._handle_register,
                                bgcolor=AppColors.PRIMARY,
                                color=AppColors.ON_PRIMARY,
                                width=float("inf"),
                                height=50,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                            ),
                            ft.TextButton(
                                "Already registered? Login",
                                on_click=self.on_go_login,
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=24,
                    expand=True,
                )
            ],
        )

    def _handle_register(self, e):
        """Handle registration form submission."""
        name = self.name_field.value.strip()
        email = self.email_field.value.strip()
        password = self.password_field.value
        phone = self.phone_field.value.strip() or None

        if not name or not email or not password:
            self.error_text.value = "Please fill in required fields"
            self.page.update()
            return

        try:
            import httpx
            from config.settings import settings
            resp = httpx.post(
                f"{settings.API_BASE_URL}/api/v1/auth/register",
                json={"full_name": name, "email": email, "password": password,
                      "phone": phone, "role": "citizen"},
                timeout=10,
            )
            if resp.status_code == 201:
                self.on_register_success()
            else:
                self.error_text.value = resp.json().get("detail", "Registration failed")
                self.page.update()
        except Exception as ex:
            self.error_text.value = f"Connection error: {ex}"
            self.page.update()
