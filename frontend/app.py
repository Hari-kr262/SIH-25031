"""
CivicResolve Flet Application
Main entry point with routing and role-based navigation.
"""

import flet as ft
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

    def route_change(e):
        """Handle route changes and render the appropriate view."""
        page.views.clear()
        route = page.route

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

        elif route == "/citizen/notifications":
            from frontend.citizen.notifications import NotificationsPage
            np = NotificationsPage(page)
            page.views.append(np.build())

        elif route == "/citizen/issues":
            from frontend.citizen.my_issues import MyIssuesPage
            mp = MyIssuesPage(
                page,
                on_view_issue=lambda issue: page.go(f"/citizen/issue/{issue.get('id')}"),
            )
            page.views.append(mp.build())

        elif route == "/citizen/map":
            from frontend.citizen.city_map import CityMapPage
            cm = CityMapPage(page)
            page.views.append(cm.build())

        elif route == "/citizen/chatbot":
            from frontend.citizen.chatbot import ChatbotPage
            cp = ChatbotPage(page)
            page.views.append(cp.build())

        elif route == "/public/dashboard":
            from frontend.common.public_dashboard import PublicDashboardPage
            pd = PublicDashboardPage(page)
            page.views.append(pd.build())

        elif route == "/citizen/leaderboard":
            from frontend.citizen.leaderboard import LeaderboardPage
            lp = LeaderboardPage(page)
            page.views.append(lp.build())

        elif route == "/citizen/profile":
            from frontend.citizen.profile import ProfilePage
            pp = ProfilePage(page)
            page.views.append(pp.build())

        elif route.startswith("/citizen/issue/"):
            from frontend.citizen.issue_detail import IssueDetailPage
            issue_id = route.split("/citizen/issue/")[-1]
            dp = IssueDetailPage(page, issue_id=issue_id)
            page.views.append(dp.build())

        elif route == "/forgot-password":
            from frontend.common.forgot_password import ForgotPasswordPage
            fp = ForgotPasswordPage(page)
            page.views.append(fp.build())

        # ----------------------------------------------------------------
        # Admin routes
        # ----------------------------------------------------------------
        elif route == "/admin/home":
            from frontend.admin.home import AdminHome
            ah = AdminHome(page)
            page.views.append(ah.build())

        elif route == "/admin/dashboard":
            from frontend.admin.dashboard import AdminDashboard
            ad = AdminDashboard(page)
            page.views.append(ad.build())

        elif route == "/admin/users":
            from frontend.admin.users import AdminUsersPage
            ap = AdminUsersPage(page)
            page.views.append(ap.build())

        elif route == "/admin/departments":
            from frontend.admin.departments import AdminDepartmentsPage
            dp = AdminDepartmentsPage(page)
            page.views.append(dp.build())

        elif route == "/admin/analytics":
            from frontend.admin.analytics import AdminAnalyticsPage
            ap = AdminAnalyticsPage(page)
            page.views.append(ap.build())

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
        if role in ("municipal_admin", "super_admin", "department_head"):
            page.go("/admin/dashboard")
        else:
            page.go("/citizen/home")

    def view_pop(e):
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
        view=ft.AppView.WEB_BROWSER,
        port=8080,
    )
