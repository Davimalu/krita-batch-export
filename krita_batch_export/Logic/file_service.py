import os
import re
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog

from krita_batch_export.Config.export_handlers import EXPORT_HANDLERS
from krita_batch_export.Config.config_service import ConfigService
from krita_batch_export.Model.png_settings import PNGSettings


class FileService:
    def __init__(self):
        self._file = None


    @staticmethod
    def get_file_path():
        """Asks the user to select a file in the GUI and returns the full path to the selected file including the file extension"""

        # Get the supported file formats from the config
        supported_file_formats = ConfigService.get_file_formats()
        file_filter = ";;".join(
            [f'{fmt["name"]} (*.{fmt["extension"]})' for fmt in supported_file_formats]
            # -> 'PNG image (*.png);;JPEG image (*.jpg);;TIFF image (*.tif)';;...
        )

        # Open a file dialog to let the user choose a base filename and format
        file_name, file_ext = QFileDialog.getSaveFileName(
            None,
            "Select base filename and format",
            "",
            file_filter
        )
        if not file_name:
            return  # User canceled

        # Get the base filename and extension
        base, ext = os.path.splitext(file_name)
        # If the file extension wasn't specified in the file name, try to determine it from the selected filter
        if not ext:
            match = re.search(r"\*\.(\w+)", file_ext) # Match the file extension in the filter, e.g. '*.png'
            if match:
                ext = '.' + match.group(1)  # extract the extension from the match, e.g. 'png'
            else:
                # If the file extension can't be determined from the filter, default to .png
                ext = '.png'

        return base, ext


    @staticmethod
    def create_export_info(ext):
        """
        Given a file extension (e.g., '.png'), opens the appropriate export dialog
        and returns an InfoObject with the export settings. Returns None if canceled or unsupported.
        """
        ext_lower = ext.lower()

        # Look up the handler for this extension (stored in export_handlers.py)
        handler = EXPORT_HANDLERS.get(ext_lower)
        if not handler:
            QMessageBox.warning(
                None,
                "Unsupported format",
                f"The {ext} file format is not supported by this plugin."
            )
            return None

        # Unpack the handler into model, view, view_model, and service classes
        model_class = handler["model"]
        view_class = handler["view"]
        view_model_class = handler["viewModel"]
        service_class = handler["service"]

        # Initialize the components
        view_model = view_model_class(model_class())
        view = view_class(view_model)

        # Open the dialog
        if view.exec_() == QDialog.Rejected:
            return None  # user canceled

        # Get the settings the user has chosen in the dialog
        settings = view.getSettings()

        # Convert the dialog settings to an InfoObject (Krita's export settings format)
        export_info = service_class.to_info_object(settings)

        return export_info