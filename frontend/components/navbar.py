"""Navigation bar component."""
import flet as ft
from frontend.themes.colors import AppColors


def BottomNavBar(selected_index: int, on_change, items: list) -> ft.NavigationBar:
    """
    Create a Material Design 3 bottom navigation bar.

    Args:
        selected_index: Currently selected item index.
        on_change: Callback when selection changes.
        items: List of dicts with 'icon' and 'label' keys.
    """
    return ft.NavigationBar(
        selected_index=selected_index,
        on_change=on_change,
        bgcolor=AppColors.BACKGROUND,
        indicator_color=AppColors.PRIMARY,
        destinations=[
            ft.NavigationBarDestination(icon=item["icon"], label=item["label"])
            for item in items
        ],
    )
