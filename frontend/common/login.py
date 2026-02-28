"""Login screen."""
import flet as ft
from frontend.themes.colors import AppColors


class LoginPage:
    """Email/password login screen."""

    def __init__(self, page: ft.Page, on_login_success, on_go_register, on_forgot_password):
        self.page = page
        self.on_login_success = on_login_success
        self.on_go_register = on_go_register
        self.on_forgot_password = on_forgot_password
        self.email_field = ft.TextField(
            label="Email", hint_text="Enter your email",
            keyboard_type=ft.KeyboardType.EMAIL, border_radius=12,
        )
        self.password_field = ft.TextField(
            label="Password", hint_text="Enter password",
            password=True, can_reveal_password=True, border_radius=12,
        )
        self.error_text = ft.Text("", color=AppColors.ERROR, size=13)

    def build(self) -> ft.View:
        return ft.View(
            route="/login",
            controls=[
                ft.AppBar(
                    title=ft.Text("Login", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                    leading=ft.IconButton("arrow_back", on_click=lambda e: self.page.go("/"),
                                         icon_color=AppColors.ON_PRIMARY),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=20),
                            ft.Text("Welcome Back 👋", size=24, weight=ft.FontWeight.BOLD),
                            ft.Text("Sign in to CivicResolve", size=14, color=AppColors.GREY),
                            ft.Container(height=20),
                            self.email_field,
                            self.password_field,
                            self.error_text,
                            ft.Container(height=8),
                            ft.ElevatedButton(
                                "Login",
                                on_click=self._handle_login,
                                bgcolor=AppColors.PRIMARY,
                                color=AppColors.ON_PRIMARY,
                                width=float("inf"),
                                height=50,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                            ),
                            ft.TextButton(
                                "Forgot Password?",
                                on_click=self.on_forgot_password,
                            ),
                            ft.Divider(),
                            ft.TextButton(
                                "Don't have an account? Register",
                                on_click=self.on_go_register,
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=24,
                    expand=True,
                )
            ],
        )

    def _handle_login(self, e):
        """Handle login form submission."""
        email = self.email_field.value.strip()
        password = self.password_field.value

        if not email or not password:
            self.error_text.value = "Please fill in all fields"
            self.page.update()
            return

        try:
            import httpx
            from config.settings import settings
            resp = httpx.post(
                f"{settings.API_BASE_URL}/api/v1/auth/login",
                json={"email": email, "password": password},
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                # Store tokens in page session
                self.page.client_storage.set("access_token", data["access_token"])
                self.page.client_storage.set("refresh_token", data["refresh_token"])
                self.page.client_storage.set("user_id", str(data["user_id"]))
                self.page.client_storage.set("user_role", data["role"])
                self.page.client_storage.set("full_name", data["full_name"])
                self.on_login_success(data["role"])
            else:
                self.error_text.value = resp.json().get("detail", "Login failed")
                self.page.update()
        except Exception as ex:
            self.error_text.value = f"Connection error: {ex}"
            self.page.update()
