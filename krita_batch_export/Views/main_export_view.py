import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QSpinBox, QFileDialog, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from krita_batch_export.ViewModel.main_export_view_model import MainExportViewModel


class MainExportView(QDialog):
    """
    The main dialog window presented to the user when batch exporting images.
    Allows the user to set export options such as path, filename, start number, file format, etc.
    """

    def __init__(self, view_model, parent=None):
        """
        Initializes the MainExportView.

        Args:
            view_model: An instance of MainExportViewModel to bind to this view.
            parent: The parent widget, if any.
        """
        super().__init__(parent)

        # Associate the View with the ViewModel
        if not isinstance(view_model, MainExportViewModel):
            raise TypeError("The view_model must be an instance of MainExportViewModel")
        self.vm = view_model

        # --- Window Setup ---
        self.setWindowTitle("Batch Export")
        self.setMinimumWidth(450)

        # Main vertical layout for the dialog
        main_layout = QVBoxLayout(self)

        # --- Setup UI ---
        self._create_widgets()
        self._layout_widgets(main_layout)
        self._style_widgets()
        self._set_initial_state()

        # --- Connect View and ViewModel ---
        self._bind_view_to_viewmodel()
        self._bind_viewmodel_to_view()
        self._update_ui_from_viewmodel()

        # TODO: Move these connections to the bind_view_to_viewmodel method and move the logic to the ViewModel
        self.browse_path_button.clicked.connect(self._on_browse_path)
        self.export_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.help_button.clicked.connect(self._on_help)

    def _create_widgets(self):
        """Creates all the widgets needed for the main export dialog"""
        # --- Export Path ---
        self.export_path_label = QLabel("Export Path:")
        self.export_path_textbox = QLineEdit()
        self.browse_path_button = QPushButton("Browse...")

        # --- Filename ---
        self.filename_label = QLabel("Filename:")
        self.filename_textbox = QLineEdit()

        self.filename_textbox.setPlaceholderText("e.g., MyImage_###")

        # --- Start Number ---
        self.start_number_label = QLabel("Start Number:")
        self.start_number_spinbox = QSpinBox()

        self.start_number_spinbox.setRange(0, 9999)
        self.start_number_spinbox.setValue(1)

        # --- File Format ---
        self.file_format_label = QLabel("File Format:")
        self.file_format_combo = QComboBox()

        # TODO: Get from ExportHandlers | Some of these are currently placeholders
        self.file_format_combo.addItems([
            "png", "jpg", "tiff", "gif", "webp"
        ])

        # --- Bottom Bar ---
        self.version_label = QLabel("Krita Batch Export v0.1.0")
        self.help_button = QPushButton("Help")
        self.export_button = QPushButton("Export")
        self.cancel_button = QPushButton("Cancel")

        self.export_button.setDefault(True)

    def _layout_widgets(self, main_layout):
        """Lays out the widgets in the dialog"""
        # --- Export Path Section ---
        main_layout.addWidget(self.export_path_label)
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.export_path_textbox)
        path_layout.addWidget(self.browse_path_button)
        main_layout.addLayout(path_layout)

        # --- Filename Section ---
        main_layout.addWidget(self.filename_label)
        main_layout.addWidget(self.filename_textbox)

        # --- Start Number Section ---
        main_layout.addWidget(self.start_number_label)
        main_layout.addWidget(self.start_number_spinbox)

        # --- File Format Section ---
        main_layout.addWidget(self.file_format_label)
        main_layout.addWidget(self.file_format_combo)

        # Add a spacer to push the bottom bar down
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # --- Bottom Bar ---
        bottom_bar_layout = QHBoxLayout()
        bottom_bar_layout.addWidget(self.version_label)
        bottom_bar_layout.addWidget(self.help_button)
        bottom_bar_layout.addStretch()  # Pushes buttons to the right
        bottom_bar_layout.addWidget(self.cancel_button)
        bottom_bar_layout.addWidget(self.export_button)
        main_layout.addLayout(bottom_bar_layout)

    def _style_widgets(self):
        """Applies basic styles to the widgets."""
        self.export_path_textbox.setReadOnly(True)

        # Style buttons
        self.export_button.setStyleSheet("background-color: #0078d7; color: white; padding: 5px;")
        self.cancel_button.setStyleSheet("background-color: #e0e0e0; padding: 5px;")
        self.help_button.setStyleSheet("background-color: #e0e0e0; padding: 5px;")
        self.browse_path_button.setStyleSheet("padding: 2px 10px;")

    def _set_initial_state(self):
        """Sets the initial state of widgets that depend on system state."""


        # TODO: Move logic to ViewModel
        # Set the default export path to the user's home directory
        home_dir = os.path.expanduser("~")
        self.export_path_textbox.setText(home_dir)

    def _bind_view_to_viewmodel(self):
        """
        Connects user interactions from the View to the ViewModel's properties and commands.
        (View -> ViewModel)
        """
        self.export_path_textbox.textChanged.connect(lambda text: setattr(self.vm, "export_path", text))
        self.filename_textbox.textChanged.connect(lambda text: setattr(self.vm, "filename", text))
        self.file_format_combo.currentTextChanged.connect(lambda text: setattr(self.vm, "file_format", text))
        self.start_number_spinbox.valueChanged.connect(lambda value: setattr(self.vm, "start_number", value))

        # Bind button clicks to ViewModel commands
        self.browse_path_button.clicked.connect(self._on_browse_path)

    def _bind_viewmodel_to_view(self):
        """
        Connects the ViewModel's property-changed signals to the View's update methods (slots).
        (ViewModel -> View)
        """
        self.vm.export_path_changed.connect(self.export_path_textbox.setText)
        self.vm.filename_changed.connect(self.filename_textbox.setText)
        self.vm.file_format_changed.connect(self.file_format_combo.setCurrentText)
        self.vm.start_number_changed.connect(self.start_number_spinbox.setValue)

    def _update_ui_from_viewmodel(self):
        """
        Updates the UI elements based on the current state of the ViewModel.
        Called once at startup to ensure the UI reflects the initial state.
        """
        self.export_path_textbox.setText(self.vm.export_path)
        self.filename_textbox.setText(self.vm.filename)
        self.file_format_combo.setCurrentText(self.vm.file_format)
        self.start_number_spinbox.setValue(self.vm.start_number)

    def _on_browse_path(self):
        """
        Opens a QFileDialog to allow the user to select an export directory.
        The selected path is then passed to the ViewModel.
        """

        # TODO: The logic for opening the file dialog should be implemented in the ViewModel, possibly using an abstraction layer to avoid having a direct dependency on QFileDialog in the ViewModel

        current_path = self.export_path_textbox.text()

        # Open the file dialog
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Export Directory",
            current_path
        )

        # If a directory was selected, update the ViewModel
        if directory and directory != current_path:
            # Update the text in the textbox and in the ViewModel
            self.export_path_textbox.setText(directory)
            setattr(self.vm, "export_path", directory)

    def _on_help(self):
        # TODO: Just a placeholder, implement in the ViewModel
        print("Help button clicked!")