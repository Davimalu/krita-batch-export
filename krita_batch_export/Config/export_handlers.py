from krita_batch_export.ViewModel.png_export_view_model import PNGExportViewModel
from krita_batch_export.Views.png_export_view import PNGExportView
from krita_batch_export.Logic.png_settings_service import PNGSettingsService
from krita_batch_export.Model.png_settings import PNGSettings

EXPORT_HANDLERS = {
    ".png": {
        "model": PNGSettings,
        "view": PNGExportView,
        "viewModel": PNGExportViewModel,
        "service": PNGSettingsService
    },
    ".jpg": {
        "view": None,  # placeholders for future classes
        "viewModel": None,
        "service": None,
    },
    ".jpeg": {
        "view": None,
        "viewModel": None,
        "service": None,
    },
    ".tif": {
        "view": None,
        "viewModel": None,
        "service": None,
    },
}
