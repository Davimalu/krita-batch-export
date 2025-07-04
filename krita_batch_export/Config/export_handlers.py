from krita_batch_export.ViewModel.png_export_view_model import PNGExportViewModel
from krita_batch_export.Views.png_export_view import PNGExportView
from krita_batch_export.KritaWrappers.png_converter_service import PNGConverterService
from krita_batch_export.Model.png_settings import PNGSettings

EXPORT_HANDLERS = {
    "png": {
        "model": PNGSettings,
        "view": PNGExportView,
        "viewModel": PNGExportViewModel,
        "converter": PNGConverterService
    },
    "jpg": {
        "view": None,  # placeholders for future classes
        "viewModel": None,
        "service": None,
    },
    "jpeg": {
        "view": None,
        "viewModel": None,
        "service": None,
    },
    "tif": {
        "view": None,
        "viewModel": None,
        "service": None,
    },
}
