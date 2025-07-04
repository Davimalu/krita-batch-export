from krita import *
from PyQt5.QtWidgets import QFileDialog, QProgressDialog, QMessageBox, QDialog, QLabel, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Import custom dialogs for supported file formats
from krita_batch_export.Logic.krita_service import KritaService
from krita_batch_export.Model.export_progress import ExportProgress
from krita_batch_export.Model.general_settings import GeneralSettings
from krita_batch_export.ViewModel.export_progress_view_model import ExportProgressViewModel
from krita_batch_export.Views.export_progress_view import ExportProgressView
from krita_batch_export.ViewModel.main_export_view_model import MainExportViewModel
from krita_batch_export.Views.main_export_view import MainExportView


class BatchExportExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        # Create a new action in Krita's file menu that will trigger the batch export
        action = window.createAction("batch_export", "Batch Export", "tools/scripts")
        action.setIcon(QIcon.fromTheme("document-export"))
        action.triggered.connect(self.batch_export)

    def batch_export(self):


        # Open the main export dialog
        main_window_settings = GeneralSettings()
        main_window_view_model = MainExportViewModel(main_window_settings)
        main_window_view = MainExportView(main_window_view_model)

        # If the user clicks "Cancel" in the main dialog, exit the batch export
        if main_window_view.exec_() != QDialog.Accepted:
            return


# Add the extension to Krita's list of extensions:
Krita.instance().addExtension(BatchExportExtension(Krita.instance()))