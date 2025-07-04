from PyQt5.QtCore import QObject, pyqtSignal

from krita_batch_export.Model.export_progress import ExportProgress

class ExportProgressViewModel(QObject):
    """ViewModel for the export progress dialog"""

    # --- Signals for Data Binding ---
    file_path_changed = pyqtSignal(str)
    total_steps_changed = pyqtSignal(int)
    current_step_changed = pyqtSignal(int)
    time_elapsed_changed = pyqtSignal(int)
    time_remaining_changed = pyqtSignal(int)

    def __init__(self, model):
        super().__init__()

        if not isinstance(model, ExportProgress):
            raise TypeError("The model must be an instance of ExportProgress")

        self._model = model

    # --- Properties for Data Binding ---
    @property
    def file_path(self):
        return self._model.file_path

    @file_path.setter
    def file_path(self, value):
        if self._model.file_path != value:
            self._model.file_path = value
            self.file_path_changed.emit(value)

    @property
    def total_steps(self):
        return self._model.total_steps

    @total_steps.setter
    def total_steps(self, value):
        if self._model.total_steps != value:
            self._model.total_steps = value
            self.total_steps_changed.emit(value)

    @property
    def current_step(self):
        return self._model.current_step

    @current_step.setter
    def current_step(self, value):
        if self._model.current_step != value:
            self._model.current_step = value
            self.current_step_changed.emit(value)

    @property
    def time_elapsed(self):
        return self._model.time_elapsed

    @time_elapsed.setter
    def time_elapsed(self, value):
        if self._model.time_elapsed != value:
            self._model.time_elapsed = value
            self.time_elapsed_changed.emit(value)

    @property
    def time_remaining(self):
        return self._model.time_remaining

    @time_remaining.setter
    def time_remaining(self, value):
        if self._model.time_remaining != value:
            self._model.time_remaining = value
            self.time_remaining_changed.emit(value)

    @property
    def time_elapsed_str(self):
        """
        Formatted string for time elapsed - depending on how much time has passed, hours, minutes, or seconds will be used
        """

        if self._model.time_elapsed >= 3600:
            return f"{self._model.time_elapsed // 3600}h {self._model.time_elapsed % 3600 // 60}m {self._model.time_elapsed % 60}s"
        elif self._model.time_elapsed >= 60:
            return f"{self._model.time_elapsed // 60}m {self._model.time_elapsed % 60}s"
        else:
            return f"{self._model.time_elapsed}s"

    @property
    def time_remaining_str(self):
        """
        Formatted string for time remaining - depending on how much time is left, hours, minutes, or seconds will be used
        """

        if self._model.time_remaining >= 3600:
            return f"{self._model.time_remaining // 3600}h {self._model.time_remaining % 3600 // 60}m {self._model.time_remaining % 60}s"
        elif self._model.time_remaining >= 60:
            return f"{self._model.time_remaining // 60}m {self._model.time_remaining % 60}s"
        else:
            return f"{self._model.time_remaining}s"