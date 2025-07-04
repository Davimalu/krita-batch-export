from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFileDialog

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