"""
CivicResolve Flet Application
Main entry point with routing and role-based navigation.
"""

import flet as ft
from config.settings import settings
from frontend.themes.colors import AppColors
from frontend.themes.light_theme import get_light_theme
from frontend.themes.dark_theme import get_dark_theme


def main(page: ft.Page):
    """Main Flet application with routing."""
    # Page configuration
    page.title = "CivicResolve"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = get_light_theme()
    page.dark_theme = get_dark_theme()
    page.window.width = 390
    page.window.height = 844
    page.fonts = {}

    def route_change(route_event: ft.RouteChangeEvent):
        """Handle route changes and render the appropriate view."""
        page.views.clear()
        route = route_event.route

        # ----------------------------------------------------------------
        # Public routes
        # ----------------------------------------------------------------
        if route == "/":
            from frontend.common.landing import LandingPage
            lp = LandingPage(
                page,
                on_login=lambda e: page.go("/login"),
                on_register=lambda e: page.go("/register"),
            )
            page.views.append(lp.build())

        elif route == "/login":
            from frontend.common.login import LoginPage
            lp = LoginPage(
                page,
                on_login_success=_navigate_by_role,
                on_go_register=lambda e: page.go("/register"),
                on_forgot_password=lambda e: page.go("/forgot-password"),
            )
            page.views.append(lp.build())

        elif route == "/register":
            from frontend.common.register import RegisterPage
            rp = RegisterPage(
                page,
                on_register_success=lambda: page.go("/login"),
                on_go_login=lambda e: page.go("/login"),
            )
            page.views.append(rp.build())

        # ----------------------------------------------------------------
        # Citizen routes
        # ----------------------------------------------------------------
        elif route == "/citizen/home":
            from frontend.citizen.home import CitizenHome
            ch = CitizenHome(
                page,
                on_report_issue=lambda e: page.go("/citizen/report"),
                on_view_issue=lambda issue: page.go(f"/citizen/issue/{issue.get('id')}"),
            )
            page.views.append(ch.build())

        elif route == "/citizen/report":
            from frontend.citizen.report_issue import ReportIssuePage
            rp = ReportIssuePage(page, on_submit_success=lambda: page.go("/citizen/home"))
            page.views.append(rp.build())

        # ----------------------------------------------------------------
        # Admin routes
        # ----------------------------------------------------------------
        elif route == "/admin/home":
            from frontend.admin.home import AdminHome
            ah = AdminHome(page)
            page.views.append(ah.build())

        # ----------------------------------------------------------------
        # Worker routes
        # ----------------------------------------------------------------
        elif route == "/worker/home":
            from frontend.worker.home import WorkerHome
            wh = WorkerHome(page, on_view_issue=lambda issue: None)
            page.views.append(wh.build())

        # ----------------------------------------------------------------
        # Fallback — redirect to landing
        # ----------------------------------------------------------------
        else:
            page.views.append(_not_found_view(page))

        page.update()

    def _navigate_by_role(role: str):
        """Navigate to the role-specific home screen after login."""
        role_routes = {
            "citizen": "/citizen/home",
            "volunteer": "/citizen/home",
            "field_worker": "/worker/home",
            "department_head": "/admin/home",
            "municipal_admin": "/admin/home",
            "super_admin": "/admin/home",
        }
        page.go(role_routes.get(role, "/citizen/home"))

    def view_pop(view: ft.View):
        """Handle back navigation."""
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route or "/")


def _not_found_view(page: ft.Page) -> ft.View:
    """404 not found view."""
    return ft.View(
        route="/404",
        controls=[
            ft.AppBar(title=ft.Text("Not Found"), bgcolor=AppColors.PRIMARY),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("🔍", size=60),
                        ft.Text("Page Not Found", size=24, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("Go Home", on_click=lambda e: page.go("/")),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=16,
                ),
                expand=True,
            ),
        ],
    )


if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.AppView.FLET_APP,
        host=settings.FLET_SERVER_HOST,
        port=settings.FLET_SERVER_PORT,
    )
