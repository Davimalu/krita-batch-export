from PyQt5.QtWidgets import QDialog

from krita_batch_export.Config.export_handlers import EXPORT_HANDLERS
from krita_batch_export.QtWrappers.message_box_service import MessageBoxService


class ExportService:
    def __init__(self):
        self._file = None


    @staticmethod
    def get_export_settings(ext):
        """
        Given a file extension (e.g., 'png'), opens the appropriate export dialog
        and returns an InfoObject with the export settings. Returns None if canceled or unsupported.
        """
        # Normalize the extension to lowercase
        ext_lower = ext.lower()

        # Look up the handler for this extension (stored in export_handlers.py)
        handler = EXPORT_HANDLERS.get(ext_lower)
        if not handler:
            MessageBoxService.show_warning(
                "Unsupported format",
                f"The {ext} file format is not supported by this plugin."
            )
            return None

        # Unpack the handler into model, view, view_model, and converter class
        model_class = handler["model"]
        view_class = handler["view"]
        view_model_class = handler["viewModel"]
        converter_class = handler["converter"]

        # Initialize the components
        view_model = view_model_class(model_class())
        view = view_class(view_model)

        # Open the dialog
        if view.exec_() == QDialog.Rejected:
            return None  # user canceled

        # Get the settings the user has chosen in the dialog
        settings = view_model.get_current_export_settings()

        # Convert the dialog settings to an InfoObject (Krita's export settings format)
        export_info = converter_class.to_info_object(settings)

        return export_info