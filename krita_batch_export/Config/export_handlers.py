from PyQt5.QtWidgets import QMessageBox, QDialog

from krita_batch_export.ExportDialogs.png_export_dialog import PNGExportDialog
from krita_batch_export.Logic.png_settings_service import PNGSettingsService
# from .jpeg_export_dialog import JPEGExportDialog
# from .jpeg_service import JPEGSettingsService
# from .tiff_export_dialog import TIFFExportDialog
# from .tiff_service import TIFFSettingsService

EXPORT_HANDLERS = {
    ".png": {
        "dialog": PNGExportDialog,
        "service": PNGSettingsService,
    },
    ".jpg": {
        "dialog": None,  # placeholders for future classes
        "service": None,
    },
    ".jpeg": {
        "dialog": None,
        "service": None,
    },
    ".tif": {
        "dialog": None,
        "service": None,
    },
}
