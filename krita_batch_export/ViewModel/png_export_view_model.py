from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor

from krita_batch_export.Model.png_settings import PNGSettings

class PNGExportViewModel(QObject):
    """ViewModel for the PNG export settings dialog"""

    # --- Signals for Data Binding ---
    # will be emitted whenever a property changes, so the view can update accordingly
    compression_changed = pyqtSignal(int)
    save_as_indexed_changed = pyqtSignal(bool)
    interlacing_changed = pyqtSignal(bool)
    save_as_hdr_changed = pyqtSignal(bool)
    embed_srgb_changed = pyqtSignal(bool)
    force_srgb_changed = pyqtSignal(bool)
    store_alpha_changed = pyqtSignal(bool)
    store_metadata_changed = pyqtSignal(bool)
    sign_with_author_changed = pyqtSignal(bool)
    force_eight_bit_changed = pyqtSignal(bool)
    transparent_color_changed = pyqtSignal(QColor)

    def __init__(self, model):
        super().__init__()

        if not isinstance(model, PNGSettings):
            raise TypeError("The model must be an instance of PNGSettings")

        self._model = model

    # --- Properties for Data Binding ---
    # These properties provide an interface for the view to bind to
    # The setter for reach property emits the corresponding signal to notify the view of the change
    @property
    def compression(self):
        return self._model.compression

    @compression.setter
    def compression(self, value):
        if self._model.compression != value:
            self._model.compression = value
            self.compression_changed.emit(value)

    @property
    def save_as_indexed(self):
        return self._model.save_as_indexed

    @save_as_indexed.setter
    def save_as_indexed(self, value):
        if self._model.save_as_indexed != value:
            self._model.save_as_indexed = value
            self.save_as_indexed_changed.emit(value)

    @property
    def interlacing(self):
        return self._model.interlacing

    @interlacing.setter
    def interlacing(self, value):
        if self._model.interlacing != value:
            self._model.interlacing = value
            self.interlacing_changed.emit(value)

    @property
    def save_as_hdr(self):
        return self._model.save_as_hdr

    @save_as_hdr.setter
    def save_as_hdr(self, value):
        if self._model.save_as_hdr != value:
            self._model.save_as_hdr = value
            self.save_as_hdr_changed.emit(value)

    @property
    def embed_srgb(self):
        return self._model.embed_srgb

    @embed_srgb.setter
    def embed_srgb(self, value):
        if self._model.embed_srgb != value:
            self._model.embed_srgb = value
            self.embed_srgb_changed.emit(value)

    @property
    def force_srgb(self):
        return self._model.force_srgb

    @force_srgb.setter
    def force_srgb(self, value):
        if self._model.force_srgb != value:
            self._model.force_srgb = value
            self.force_srgb_changed.emit(value)

    @property
    def store_alpha(self):
        return self._model.store_alpha

    @store_alpha.setter
    def store_alpha(self, value):
        if self._model.store_alpha != value:
            self._model.store_alpha = value
            self.store_alpha_changed.emit(value)

    @property
    def store_metadata(self):
        return self._model.store_metadata

    @store_metadata.setter
    def store_metadata(self, value):
        if self._model.store_metadata != value:
            self._model.store_metadata = value
            self.store_metadata_changed.emit(value)

    @property
    def sign_with_author(self):
        return self._model.sign_with_author

    @sign_with_author.setter
    def sign_with_author(self, value):
        if self._model.sign_with_author != value:
            self._model.sign_with_author = value
            self.sign_with_author_changed.emit(value)

    @property
    def force_eight_bit(self):
        return self._model.force_eight_bit

    @force_eight_bit.setter
    def force_eight_bit(self, value):
        if self._model.force_eight_bit != value:
            self._model.force_eight_bit = value
            self.force_eight_bit_changed.emit(value)

    @property
    def transparent_color(self):
        return QColor(
            self._model.transparent_color_R,
            self._model.transparent_color_G,
            self._model.transparent_color_B
        )

    @transparent_color.setter
    def transparent_color(self, qColor_value):
        new_color = (qColor_value.red(), qColor_value.green(), qColor_value.blue())
        current_color = (
            self._model.transparent_color_R,
            self._model.transparent_color_G,
            self._model.transparent_color_B
        )
        if current_color != new_color:
            self._model.transparent_color_R = new_color[0]
            self._model.transparent_color_G = new_color[1]
            self._model.transparent_color_B = new_color[2]
            self.transparent_color_changed.emit(qColor_value)

    # --- Commands ---

    # -- Additional logic ---
    def get_current_export_settings(self):
        """
        Returns the current export settings as a PNGSettings object.

        Returns:
            PNGSettings: The current export settings.
        """
        return self._model