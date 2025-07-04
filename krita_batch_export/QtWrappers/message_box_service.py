from PyQt5.QtWidgets import QMessageBox

class MessageBoxService:
    """
    Wrapper for displaying messages via QMessageBox to avoid direct dependencies on PyQt5 in the rest of the codebase
    """

    def __init__(self):
        pass


    @staticmethod
    def show_warning(title: str, message: str, parent=None) -> None:
        """
        Displays a warning message box with the given title and message

        :param title: The title of the message box
        :param message: The message to display in the message box
        :param parent: The parent widget for the message box, if any
        """
        QMessageBox.warning(
            parent,
            title,
            message
        )

    @staticmethod
    def show_info(title: str, message: str, parent=None) -> None:
        """
        Displays an information message box with the given title and message

        :param title: The title of the message box
        :param message: The message to display in the message box
        :param parent: The parent widget for the message box, if any
        """
        QMessageBox.information(
            parent,
            title,
            message
        )

    @staticmethod
    def show_error(title: str, message: str, parent=None) -> None:
        """
        Displays an error message box with the given title and message

        :param title: The title of the message box
        :param message: The message to display in the message box
        :param parent: The parent widget for the message box, if any
        """

        QMessageBox.critical(
            parent,
            title,
            message
        )