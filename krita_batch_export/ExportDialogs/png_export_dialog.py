from krita import *
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QCheckBox, QPushButton, QColorDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from krita_batch_export.Helper.color_helper import RGB_to_krita_color_format

class PNGExportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PNG Export Settings")

        main_layout = QVBoxLayout(self)

        # --- Compression Section ---

        # Compression Label
        compression_label = QLabel("Compression (Lossless):")
        main_layout.addWidget(compression_label)

        # Slider
        slider_layout = QHBoxLayout()
        self.compression_slider = QSlider(Qt.Horizontal)
        self.compression_slider.setRange(0, 9)
        self.compression_slider.setValue(3)  # Default compression level
        slider_layout.addWidget(self.compression_slider)
        main_layout.addLayout(slider_layout)

        # Labels for "Large file size" and "Small file size"
        size_label_layout = QHBoxLayout()
        size_label_layout.addWidget(QLabel("Large file size"))
        size_label_layout.addStretch()
        size_label_layout.addWidget(QLabel("Small file size"))
        main_layout.addLayout(size_label_layout)

        # --- Checkboxes ---
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

        main_layout.addWidget(self.save_as_indexed_check)
        main_layout.addWidget(self.interlacing_check)
        main_layout.addWidget(self.save_as_hdr_check)
        main_layout.addWidget(self.embed_srgb_check)
        main_layout.addWidget(self.force_srgb_check)
        main_layout.addWidget(self.store_alpha_check)
        main_layout.addWidget(self.store_metadata_check)
        main_layout.addWidget(self.sign_with_author_check)
        main_layout.addWidget(self.force_eight_bit_check)

        # --- Transparent Color ---
        transparent_color_layout = QHBoxLayout()
        transparent_color_label = QLabel("Transparent color:")
        self.transparent_color_button = QPushButton("Select Color")
        self.transparent_color_button.clicked.connect(self._on_select_color)
        transparent_color_layout.addWidget(transparent_color_label)
        transparent_color_layout.addWidget(self.transparent_color_button)
        main_layout.addLayout(transparent_color_layout)

        # Variables to store the transparent color
        self.transparent_color_R = 255
        self.transparent_color_G = 255
        self.transparent_color_B = 255

        # --- OK/Cancel Buttons ---
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)


    def _on_select_color(self):
        """Pop up a color picker to select the transparent color."""
        color = QColorDialog.getColor(Qt.transparent, self, "Select Transparent Color")
        if color.isValid():
            self.transparent_color_R = color.red()
            self.transparent_color_G = color.green()
            self.transparent_color_B = color.blue()


    def getSettings(self):
        """Return a dictionary of the user's chosen settings"""
        return {
            "compression": self.compression_slider.value(),
            "save_as_indexed": self.save_as_indexed_check.isChecked(),
            "interlacing": self.interlacing_check.isChecked(),
            "save_as_hdr": self.save_as_hdr_check.isChecked(),
            "embed_srgb": self.embed_srgb_check.isChecked(),
            "force_srgb": self.force_srgb_check.isChecked(),
            "store_alpha": self.store_alpha_check.isChecked(),
            "store_metadata": self.store_metadata_check.isChecked(),
            "sign_with_author": self.sign_with_author_check.isChecked(),
            "force_eight_bit": self.force_eight_bit_check.isChecked(),
            "transparent_color_R": self.transparent_color_R,
            "transparent_color_G": self.transparent_color_G,
            "transparent_color_B": self.transparent_color_B,
        }


    def getInfoObject(self):
        """Return an InfoObject() containing the user's chosen settings"""
        exportInfo = InfoObject()
        settings = self.getSettings()

        # Populate the InfoObject for PNG export
        exportInfo.setProperty("alpha", settings["store_alpha"])
        exportInfo.setProperty("compression", settings["compression"])
        exportInfo.setProperty("forceSRGB", settings["force_srgb"])
        exportInfo.setProperty("indexed", settings["save_as_indexed"])
        exportInfo.setProperty("interlaced", settings["interlacing"])
        exportInfo.setProperty("saveAsHDR", settings["save_as_hdr"])
        exportInfo.setProperty("saveSRGBProfile", settings["embed_srgb"])
        exportInfo.setProperty("storeAuthor", settings["sign_with_author"])
        exportInfo.setProperty("storeMetaData", settings["store_metadata"])
        exportInfo.setProperty("transparencyFillcolor", RGB_to_krita_color_format([settings["transparent_color_R"], settings["transparent_color_G"], settings["transparent_color_B"]]))

        return exportInfo