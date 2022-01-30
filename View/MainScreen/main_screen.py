from typing import NoReturn

from View.base_screen import BaseScreenView


class MainScreenView(BaseScreenView):
    """Implements the login start screen in the user application."""

    def model_is_changed(self) -> NoReturn:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

        