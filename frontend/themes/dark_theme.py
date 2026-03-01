"""Dark theme configuration for Flet."""
import flet as ft
from frontend.themes.colors import AppColors


def get_dark_theme() -> ft.Theme:
    """Return CivicResolve dark theme."""
    return ft.Theme(
        color_scheme_seed=AppColors.PRIMARY,
        visual_density=ft.VisualDensity.COMFORTABLE,
        brightness=ft.Brightness.DARK,
    )
