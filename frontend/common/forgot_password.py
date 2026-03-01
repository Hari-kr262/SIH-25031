"""Forgot password screen."""
import flet as ft
from frontend.themes.colors import AppColors


class ForgotPasswordPage:
    """Password reset request screen."""

    def __init__(self, page: ft.Page, **kwargs):
        self.page = page
        self.email_field = ft.TextField(
            label="Email Address",
            hint_text="Enter your registered email",
            keyboard_type=ft.KeyboardType.EMAIL,
            border_radius=12,
            prefix_icon=ft.icons.EMAIL_OUTLINED,
        )
        self.status_text = ft.Text("", color=AppColors.SUCCESS, size=13)
        self.error_text = ft.Text("", color=AppColors.ERROR, size=13)
        self._submitted = False

    def build(self) -> ft.View:
        self._submit_btn = ft.ElevatedButton(
            "Send Reset Link",
            on_click=self._handle_submit,
            bgcolor=AppColors.PRIMARY,
            color=AppColors.ON_PRIMARY,
            width=float("inf"),
            height=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        )
        return ft.View(
            route="/forgot-password",
            controls=[
                ft.AppBar(
                    title=ft.Text("Forgot Password", color=AppColors.ON_PRIMARY),
                    bgcolor=AppColors.PRIMARY,
                    leading=ft.IconButton(
                        ft.icons.ARROW_BACK,
                        on_click=lambda e: self.page.go("/login"),
                        icon_color=AppColors.ON_PRIMARY,
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=24),
                            ft.Container(
                                content=ft.Icon(ft.icons.LOCK_RESET, size=64, color=AppColors.PRIMARY),
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(height=16),
                            ft.Text(
                                "Reset your password",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "Enter your email address and we'll send\nyou a link to reset your password.",
                                size=14,
                                color=AppColors.GREY,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(height=24),
                            self.email_field,
                            self.error_text,
                            self.status_text,
                            ft.Container(height=8),
                            self._submit_btn,
                            ft.Container(height=8),
                            ft.TextButton(
                                "Back to Login",
                                on_click=lambda e: self.page.go("/login"),
                                style=ft.ButtonStyle(color=AppColors.PRIMARY),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    expand=True,
                    padding=ft.padding.symmetric(horizontal=28, vertical=16),
                ),
            ],
        )

    def _handle_submit(self, e):
        """Send password reset link."""
        email = self.email_field.value.strip()
        if not email:
            self.error_text.value = "Please enter your email address"
            self.status_text.value = ""
            self.page.update()
            return

        try:
            import httpx
            from config.settings import settings
            resp = httpx.post(
                f"{settings.API_BASE_URL}/api/v1/auth/forgot-password",
                json={"email": email},
                timeout=10,
            )
            if resp.status_code in (200, 201, 204):
                self.status_text.value = "✅ Reset link sent! Check your inbox."
                self.error_text.value = ""
                self._submit_btn.disabled = True
            else:
                detail = resp.json().get("detail", "Request failed. Please try again.")
                self.error_text.value = detail
                self.status_text.value = ""
        except Exception:
            # Show a generic error so the user isn't misled if the service is down
            self.error_text.value = "Service temporarily unavailable. Please try again later."
            self.status_text.value = ""
        self.page.update()
