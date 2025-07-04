import os
import time

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication

from krita_batch_export.Logic.export_service import ExportService
from krita_batch_export.Model.export_progress import ExportProgress
from krita_batch_export.ViewModel.export_progress_view_model import ExportProgressViewModel
from krita_batch_export.Views.export_progress_view import ExportProgressView
from krita_batch_export.Logic.krita_service import KritaService
from krita_batch_export.Model.general_settings import GeneralSettings

class MainExportViewModel(QObject):
    """ViewModel for the main export settings dialog"""

    # --- Signals for Data Binding ---
    export_path_changed = pyqtSignal(str)
    filename_changed = pyqtSignal(str)
    file_format_changed = pyqtSignal(str)
    start_number_changed = pyqtSignal(int)

    def __init__(self, model):
        super().__init__()

        if not isinstance(model, GeneralSettings):
            raise TypeError("The model must be an instance of GeneralSettings")

        self._model = model

        # Set the default export path to the user's home directory
        self.export_path = os.path.expanduser("~")

    # --- Properties for Data Binding ---
    @property
    def  export_path(self):
        return self._model.export_path

    @export_path.setter
    def export_path(self, value):
        if self._model.export_path != value:
            self._model.export_path = value
            self.export_path_changed.emit(value)

    @property
    def filename(self):
        return self._model.filename

    @filename.setter
    def filename(self, value):
        if self._model.filename != value:
            self._model.filename = value
            self.filename_changed.emit(value)

    @property
    def file_format(self):
        return self._model.file_format

    @file_format.setter
    def file_format(self, value):
        if self._model.file_format != value:
            self._model.file_format = value
            self.file_format_changed.emit(value)

    @property
    def start_number(self):
        return self._model.start_number

    @start_number.setter
    def start_number(self, value):
        if self._model.start_number != value:
            self._model.start_number = value
            self.start_number_changed.emit(value)

    # --- Commands ---

    @pyqtSlot()
    def execute_select_export_path(self):
        """
        Opens a file dialog where the user can select the export path where the images will be saved.
        Updates the export_path property in the ViewModel with the selected directory.
        """

        # TODO: Use an abstraction layer to get rid of the direct dependency on QFileDialog
        current_path = self.export_path

        # Open the file dialog
        directory = QFileDialog.getExistingDirectory(
            None,
            "Select Export Directory",
            self.export_path
        )

        # If a directory was selected, update the export path
        if directory and directory != current_path:
            self.export_path = directory

            # Notify the UI about the change
            self.export_path_changed.emit(directory)

    @pyqtSlot()
    def execute_bug_report(self):
        """
        Opens the default web browser to the project's GitHub issues page for bug reporting.
        """
        import webbrowser
        webbrowser.open("https://github.com/Davimalu/krita-batch-export/issues/new")

    @pyqtSlot()
    def execute_start_export(self):
        """
        TODO: Write documentation
        """

        # TODO: Refactor this, break dependencies

        # If the user hasn't set an export path, throw an error | TODO: Handle gracefully in the UI
        if not self.export_path:
            raise ValueError("Export path is not set. Please select a valid export directory.")

        # If the user hasn't set a filename, throw an error | TODO: Handle gracefully in the UI
        if not self.filename:
            raise ValueError("Filename is not set. Please enter a valid filename.")

        # Get a list of all open documents in Krita
        docs = KritaService.get_all_open_documents()
        if not docs:
            QMessageBox.information(None, "Batch Export", "No documents open") # TODO: Use a Service for this
            return

        # Open the appropriate export dialog based on the selected file format (for the selection of compression level, etc.) and get the export settings as a Krita InfoObject
        export_info = ExportService.get_export_settings(self.file_format)
        if not export_info:
            return  # user canceled or unsupported format

        # Prepare a progress dialog
        progress_bar_settings = ExportProgress(self.export_path)
        progress_bar_view_model = ExportProgressViewModel(progress_bar_settings)
        progress_bar_view = ExportProgressView(progress_bar_view_model)

        # Start a timer to measure the time taken for the export
        start_time = time.time()
        elapsed_time = 0
        estimated_time_remaining = 0

        # Iterate through all open documents and export them
        for index, doc in enumerate(docs, start=1):
            # Abort the export if the user clicked "Cancel" in the progress dialog
            # TODO

            # Create a unique filename for each file by appending it with an ascending number
            export_file_name = f"{self.filename}_{self.start_number + index - 1:03d}.{self.file_format}"

            # Update the progress dialog
            progress_bar_view_model.file_path = os.path.join(self.export_path, export_file_name)
            progress_bar_view_model.total_steps = len(docs)
            progress_bar_view_model.current_step = index
            progress_bar_view_model.time_elapsed = int(elapsed_time)
            progress_bar_view_model.time_remaining = int(estimated_time_remaining)

            # Process GUI events | If this isn't done, the export loop monopolizes the main thread and the GUI can't render properly
            QApplication.processEvents()

            # Export the document with the specified settings
            doc.setBatchmode(True)  # disable popups while saving
            success = doc.exportImage(export_file_name, export_info)
            if not success:
                print(f"Failed to export '{doc.name()}'")

            doc.setBatchmode(False)  # re-enable popups

            # Calculate elapsed time
            elapsed_time = time.time() - start_time
            # Calculate estimated time remaining based on the progress so far
            estimated_time_remaining = (elapsed_time / index) * (len(docs) - index)

        # Complete the progress dialog and close it
        progress_bar_view_model.total_steps = len(docs)
        progress_bar_view_model.current_step = len(docs)
        progress_bar_view_model.time_elapsed = int(elapsed_time)
        progress_bar_view_model.time_remaining = int(estimated_time_remaining)
        progress_bar_view.close()