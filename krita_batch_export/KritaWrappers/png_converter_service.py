from krita import InfoObject

from krita_batch_export.Logic.color_service import ColorService
from krita_batch_export.Model.png_settings import PNGSettings


class PNGConverterService:
    @staticmethod
    def to_info_object(settings: PNGSettings):
        """
        Converts the PNGSettings Model to a Krita InfoObject() containing the user's chosen settings

        Args:
            settings (PNGSettings): The settings chosen by the user in the PNG export dialog

        Returns:
            InfoObject: An InfoObject containing the export settings for PNG (Krita specific object)
        """
        export_info = InfoObject()

        # Populate the InfoObject for PNG export
        export_info.setProperty("alpha", settings.store_alpha)
        export_info.setProperty("compression", settings.compression)
        export_info.setProperty("forceSRGB", settings.force_srgb)
        export_info.setProperty("indexed", settings.save_as_indexed)
        export_info.setProperty("interlaced", settings.interlacing)
        export_info.setProperty("saveAsHDR", settings.save_as_hdr)
        export_info.setProperty("saveSRGBProfile", settings.embed_srgb)
        export_info.setProperty("storeAuthor", settings.sign_with_author)
        export_info.setProperty("storeMetaData", settings.store_metadata)
        export_info.setProperty(
            "transparencyFillcolor",
            ColorService.RGB_to_krita_color_format(
                [settings.transparent_color_R, settings.transparent_color_G, settings.transparent_color_B]
            ),
        )

        return export_info