from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QSpacerItem, QSizePolicy, QPushButton
)
from PyQt5.QtCore import Qt
from krita_batch_export.ViewModel.export_progress_view_model import ExportProgressViewModel


class ExportProgressView(QDialog):
    """
    The dialog window that shows the current progress of the batch export.
    It displays the currently processed file, an overall progress bar, time estimations and a Cancel button.
    """

    def __init__(self, view_model, parent=None):
        """
        Initializes the ExportProgressView.

        Args:
            view_model: An instance of ExportProgressViewModel to bind to this view.
            parent: The parent widget, if any.
        """
        super().__init__(parent)

        # Associate the View with the ViewModel
        if not isinstance(view_model, ExportProgressViewModel):
            raise TypeError("The view_model must be an instance of ExportProgressViewModel")
        self.vm = view_model

        # --- Window Setup ---
        self.setWindowTitle("Exporting Images...")
        self.setMinimumWidth(400)

        # Make the dialog modal, so the user cannot interact with the main window
        self.setModal(True)

        # Remove the close button (question mark button is also removed)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint & ~Qt.WindowCloseButtonHint)

        # Main vertical layout for the dialog
        main_layout = QVBoxLayout(self)

        # --- Setup UI ---
        self._create_widgets()
        self._layout_widgets(main_layout)
        self._style_widgets()

        # --- Connect View and ViewModel ---
        self._bind_view_to_viewmodel()
        self._bind_viewmodel_to_view()
        self._update_ui_from_viewmodel()

    def _create_widgets(self):
        """Creates all the widgets needed for the progress dialog."""
        self.info_label = QLabel("Now exporting:")
        self.file_path_label = QLabel("")

        self.progress_bar = QProgressBar()

        self.time_elapsed_label = QLabel("Time elapsed: --")
        self.time_remaining_label = QLabel("Time remaining: --")

        self.cancel_button = QPushButton("Cancel")

    def _layout_widgets(self, main_layout):
        """Lays out the widgets in the dialog."""
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.file_path_label)

        main_layout.addSpacerItem(QSpacerItem(1, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        main_layout.addWidget(self.progress_bar)
        main_layout.addSpacerItem(QSpacerItem(1, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Layout for time labels
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.time_elapsed_label)
        time_layout.addStretch()
        time_layout.addWidget(self.time_remaining_label)
        main_layout.addLayout(time_layout)

        # Add a spacer to push the button down
        main_layout.addSpacerItem(QSpacerItem(1, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Cancel Button
        cancel_layout = QHBoxLayout()
        cancel_layout.addStretch()
        cancel_layout.addWidget(self.cancel_button)
        cancel_layout.addStretch()
        main_layout.addLayout(cancel_layout)

    def _style_widgets(self):
        """Applies basic styles to the widgets."""
        pass

    def _bind_view_to_viewmodel(self):
        """
        Connects user interactions from the View to the ViewModel's properties and commands.
        (View -> ViewModel)
        """
        self.cancel_button.clicked.connect(self.vm.cancel_export)

    def _bind_viewmodel_to_view(self):
        """
        Connects the ViewModel's property-changed signals to the View's update methods (slots).
        (ViewModel -> View)
        """
        self.vm.file_path_changed.connect(self._update_file_path)
        self.vm.total_steps_changed.connect(self.progress_bar.setMaximum)
        self.vm.current_step_changed.connect(self.progress_bar.setValue)
        self.vm.time_elapsed_changed.connect(self._update_time_elapsed)
        self.vm.time_remaining_changed.connect(self._update_time_remaining)

    def _update_ui_from_viewmodel(self):
        """
        Updates the UI elements based on the current state of the ViewModel.
        Called once at startup to ensure the UI reflects the initial state.
        """
        self._update_file_path(self.vm.file_path)
        self.progress_bar.setMaximum(self.vm.total_steps)
        self.progress_bar.setValue(self.vm.current_step)
        self._update_time_elapsed()
        self._update_time_remaining()


    # --- Helper Methods for UI Updates ---
    def _update_file_path(self, file_path):
        """
        Updates the file path label, eliding the text if it's too long.
        """

        # Elide long file paths to prevent the dialog from becoming too wide
        # We need QFontMetrics to do this, so we just get it from the label's font
        font_metrics = self.file_path_label.fontMetrics()
        elided_text = font_metrics.elidedText(file_path, Qt.ElideMiddle, self.width() - 20)  # Subtract some padding
        self.file_path_label.setText(elided_text)

    def _update_time_elapsed(self):
        """
        Updates the time elapsed label using the formatted string from the ViewModel.
        """
        self.time_elapsed_label.setText(f"Time elapsed: {self.vm.time_elapsed_str}")

    def _update_time_remaining(self):
        """
        Updates the time remaining label using the formatted string from the ViewModel.
        """
        self.time_remaining_label.setText(f"Time remaining: {self.vm.time_remaining_str}")

