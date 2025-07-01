from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QCheckBox, QPushButton, QColorDialog
)
from PyQt5.QtCore import Qt

from krita_batch_export.Model.png_settings import PNGSettings
from krita_batch_export.ViewModel.png_export_view_model import PNGExportViewModel


class PNGExportView(QDialog):
    """Dialog for setting PNG export options"""
    def __init__(self, view_model, parent=None):
        super().__init__(parent)

        # Associate the View with the ViewModel
        if not isinstance(view_model, PNGExportViewModel):
            raise TypeError("The view_model must be an instance of PNGExportViewModel")
        self.vm = view_model

        # --- Window Setup ---
        self.setWindowTitle("PNG Export Settings")
        self.setGeometry(100, 100, 450, 400)

        # Main vertical layout for the dialog
        main_layout = QVBoxLayout(self)

        # --- Setup UI ---
        self._create_widgets()
        self._layout_widgets(main_layout)
        self._style_widgets()

        # --- Connect View and ViewModel ---
        self._bind_view_to_viewmodel()
        self._bind_viewmodel_to_view()

        # TODO: Use logic in the ViewModel instead
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def _create_widgets(self):
        """Creates the widgets for the PNG export dialog"""
        # Compression Slider
        self.compression_label = QLabel("Compression (Lossless):")
        self.compression_slider = QSlider(Qt.Horizontal)
        self.compression_slider.setRange(0, 9)
        self.compression_slider.setValue(3)

        # "Large file size" / "Small file size" labels
        self.large_file_label = QLabel("Large file size")
        self.small_file_label = QLabel("Small file size")

        # Checkboxes
        self.save_as_indexed_check = QCheckBox("Save as indexed PNG, if possible")
        self.interlacing_check = QCheckBox("Interlacing")
        self.save_as_hdr_check = QCheckBox("Save as HDR image (Rec. 2020 PQ)")
        self.embed_srgb_check = QCheckBox("Embed sRGB profile")
        self.force_srgb_check = QCheckBox("Force convert to sRGB")
        self.store_alpha_check = QCheckBox("Store alpha channel (transparency)")
        self.store_metadata_check = QCheckBox("Store Metadata")
        self.sign_with_author_check = QCheckBox("Sign with author data")
        self.force_eight_bit_check = QCheckBox("Force convert to 8 bits/channel")

        # Checkboxes checked by default
        self.embed_srgb_check.setChecked(True)

        # Transparent Color Button
        self.transparent_color_label = QLabel("Transparent color:")
        self.transparent_color_button = QPushButton("Select Color")

        # Variables to store the transparent color
        self.transparent_color_R = 255
        self.transparent_color_G = 255
        self.transparent_color_B = 255

        # OK/Cancel Buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

    def _layout_widgets(self, main_layout):
        """Layouts the widgets in the dialog"""

        # Compression Section
        main_layout.addWidget(self.compression_label)
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.compression_slider)
        main_layout.addLayout(slider_layout)

        # Size Labels
        size_label_layout = QHBoxLayout()
        size_label_layout.addWidget(self.large_file_label)
        size_label_layout.addStretch()
        size_label_layout.addWidget(self.small_file_label)
        main_layout.addLayout(size_label_layout)

        # Checkboxes
        main_layout.addWidget(self.save_as_indexed_check)
        main_layout.addWidget(self.interlacing_check)
        main_layout.addWidget(self.save_as_hdr_check)
        main_layout.addWidget(self.embed_srgb_check)
        main_layout.addWidget(self.force_srgb_check)
        main_layout.addWidget(self.store_alpha_check)
        main_layout.addWidget(self.store_metadata_check)
        main_layout.addWidget(self.sign_with_author_check)
        main_layout.addWidget(self.force_eight_bit_check)

        # Transparent Color Section
        transparent_color_layout = QHBoxLayout()
        transparent_color_layout.addWidget(self.transparent_color_label)
        transparent_color_layout.addWidget(self.transparent_color_button)
        main_layout.addLayout(transparent_color_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

    def _style_widgets(self):
        """Applies styles to the widgets in the dialog"""
        # Set styles for the compression slider
        self.compression_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #f0f0f0;
                height: 8px;
            }
            QSlider::handle:horizontal {
                background: #0078d7;
                width: 16px;
                margin: -4px 0;
            }
        """)

        # Set styles for buttons
        self.ok_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.cancel_button.setStyleSheet("background-color: #f44336; color: white;")
        self.transparent_color_button.setStyleSheet("background-color: #e0e0e0;")


    def _bind_view_to_viewmodel(self):
        """
        Connects user interactions from the View (e.g., clicks, value changes) to the ViewModel's properties and commands.
        View -> ViewModel
        """

        # Bind widget interactions to ViewModel properties
        self.compression_slider.valueChanged.connect(lambda value: setattr(self.vm, "compression", value))
        self.save_as_indexed_check.toggled.connect(lambda checked: setattr(self.vm, "save_as_indexed", checked))
        self.interlacing_check.toggled.connect(lambda checked: setattr(self.vm, "interlacing", checked))
        self.save_as_hdr_check.toggled.connect(lambda checked: setattr(self.vm, "save_as_hdr", checked))
        self.embed_srgb_check.toggled.connect(lambda checked: setattr(self.vm, "embed_srgb", checked))
        self.force_srgb_check.toggled.connect(lambda checked: setattr(self.vm, "force_srgb", checked))
        self.store_alpha_check.toggled.connect(lambda checked: setattr(self.vm, "store_alpha", checked))
        self.store_metadata_check.toggled.connect(lambda checked: setattr(self.vm, "store_metadata", checked))
        self.sign_with_author_check.toggled.connect(lambda checked: setattr(self.vm, "sign_with_author", checked))
        self.force_eight_bit_check.toggled.connect(lambda checked: setattr(self.vm, "force_eight_bit", checked))

        # Bind button clicks to ViewModel commands
        self.transparent_color_button.clicked.connect(self._on_select_color) # Strictly speaking, not part of the ViewModel, but I'd like to bind all logic here for clarity
        # TODO: Implement ViewModel commands

    def _bind_viewmodel_to_view(self):
        """
        Connects the ViewModel's property-changed signals to the View's update methods (slots).
        ViewModel -> View
        """

        self.vm.compression_changed.connect(self.compression_slider.setValue)
        self.vm.save_as_indexed_changed.connect(self.save_as_indexed_check.setChecked)
        self.vm.interlacing_changed.connect(self.interlacing_check.setChecked)
        self.vm.save_as_hdr_changed.connect(self.save_as_hdr_check.setChecked)
        self.vm.embed_srgb_changed.connect(self.embed_srgb_check.setChecked)
        self.vm.force_srgb_changed.connect(self.force_srgb_check.setChecked)
        self.vm.store_alpha_changed.connect(self.store_alpha_check.setChecked)
        self.vm.store_metadata_changed.connect(self.store_metadata_check.setChecked)
        self.vm.sign_with_author_changed.connect(self.sign_with_author_check.setChecked)
        self.vm.force_eight_bit_changed.connect(self.force_eight_bit_check.setChecked)

    def _update_ui_from_viewmodel(self):
        """
        Updates the UI elements based on the current state of the ViewModel.
        Called once at startup to ensure the UI reflects the initial state.
        """

        self.compression_slider.setValue(self.vm.compression)
        self.save_as_indexed_check.setChecked(self.vm.save_as_indexed)
        self.interlacing_check.setChecked(self.vm.interlacing)
        self.save_as_hdr_check.setChecked(self.vm.save_as_hdr)
        self.embed_srgb_check.setChecked(self.vm.embed_srgb)
        self.force_srgb_check.setChecked(self.vm.force_srgb)
        self.store_alpha_check.setChecked(self.vm.store_alpha)
        self.store_metadata_check.setChecked(self.vm.store_metadata)
        self.sign_with_author_check.setChecked(self.vm.sign_with_author)
        self.force_eight_bit_check.setChecked(self.vm.force_eight_bit)

    def _on_select_color(self):
        """Pop up a color picker to select the transparent color"""
        color = QColorDialog.getColor(Qt.transparent, self, "Select Transparent Color")

        if color.isValid():
            self.transparent_color_R = color.red()
            self.transparent_color_G = color.green()
            self.transparent_color_B = color.blue()


    # TODO: Get rid of this method, use the ViewModel instead
    def getSettings(self):
        """Returns the user's chosen settings for the PNG export"""
        return PNGSettings(
            compression=self.vm.compression,
            save_as_indexed=self.vm.save_as_indexed,
            interlacing=self.vm.interlacing,
            save_as_hdr=self.vm.save_as_hdr,
            embed_srgb=self.vm.embed_srgb,
            force_srgb=self.vm.force_srgb,
            store_alpha=self.vm.store_alpha,
            store_metadata=self.vm.store_metadata,
            sign_with_author=self.vm.sign_with_author,
            force_eight_bit=self.vm.force_eight_bit,
            transparent_color_R=self.transparent_color_R,
            transparent_color_G=self.transparent_color_G,
            transparent_color_B=self.transparent_color_B
        )