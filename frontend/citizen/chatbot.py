"""Chatbot screen — AI-powered civic assistant chat interface."""
import flet as ft
from frontend.themes.colors import AppColors
from frontend.common import api_client

_WELCOME_MESSAGE = (
    "Hi! I'm CivicBot 🤖. I can help you report civic issues, "
    "track your reports, or explain the platform. What do you need?"
)
_ERROR_MESSAGE = "Sorry, I'm having trouble connecting. Please try again."


class ChatbotPage:
    """AI-powered civic assistant chatbot."""

    def __init__(self, page: ft.Page, **kwargs):
        self.page = page
        self._messages: list[dict] = []
        self._message_list = ft.Column(
            controls=[],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=8,
        )
        self._input = ft.TextField(
            hint_text="Type a message…",
            expand=True,
            border_color=AppColors.DIVIDER,
            focused_border_color=AppColors.PRIMARY,
            on_submit=self._handle_send,
        )

    def build(self) -> ft.View:
        """Build and return the Chatbot view."""
        # Show the welcome bot message on load
        self._add_message("bot", _WELCOME_MESSAGE)
        return ft.View(
            route="/citizen/chatbot",
            controls=[
                ft.AppBar(
                    title=ft.Text("AI Assistant", color=AppColors.ON_PRIMARY),
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
                            # Scrollable message area
                            ft.Container(
                                content=self._message_list,
                                expand=True,
                                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                            ),
                            ft.Divider(height=1, color=AppColors.DIVIDER),
                            # Input row
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        self._input,
                                        ft.IconButton(
                                            ft.Icons.SEND,
                                            icon_color=AppColors.PRIMARY,
                                            tooltip="Send",
                                            on_click=self._handle_send,
                                        ),
                                    ],
                                    spacing=8,
                                ),
                                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                            ),
                        ],
                        expand=True,
                    ),
                    expand=True,
                ),
            ],
        )

    def _add_message(self, sender: str, text: str):
        """Append a message bubble to the chat list."""
        is_user = (sender == "user")
        bubble = ft.Container(
            content=ft.Column(
                controls=(
                    [ft.Text(text, color=AppColors.ON_PRIMARY, size=14, selectable=True)]
                    if is_user
                    else [
                        ft.Text("🤖 CivicBot", size=11, color=AppColors.GREY,
                                weight=ft.FontWeight.W_500),
                        ft.Text(text, color=AppColors.TEXT_PRIMARY, size=14, selectable=True),
                    ]
                ),
                spacing=4,
            ),
            bgcolor=AppColors.PRIMARY if is_user else AppColors.SURFACE,
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            border_radius=ft.border_radius.only(
                top_left=16, top_right=16,
                bottom_left=4 if is_user else 16,
                bottom_right=16 if is_user else 4,
            ),
            max_width=260,
        )
        self._message_list.controls.append(
            ft.Row(
                controls=[bubble],
                alignment=(
                    ft.MainAxisAlignment.END if is_user
                    else ft.MainAxisAlignment.START
                ),
            )
        )

    def _handle_send(self, e):
        """Send user message and fetch bot response."""
        text = self._input.value.strip()
        if not text:
            return
        self._input.value = ""
        self._add_message("user", text)
        self.page.update()
        self._fetch_bot_response(text)

    def _fetch_bot_response(self, user_text: str):
        """Call chatbot API and add bot reply."""
        try:
            token = self.page.client_storage.get("access_token")
            resp = api_client.post(
                "/chatbot/message",
                data={"message": user_text},
                token=token,
            )
            if resp is not None and getattr(resp, "status_code", None) == 200:
                reply = resp.json().get("reply") or resp.json().get("message") or _ERROR_MESSAGE
            else:
                reply = _ERROR_MESSAGE
        except Exception:
            reply = _ERROR_MESSAGE
        self._add_message("bot", reply)
        self.page.update()
