from krita import *

from krita_batch_export.Logic.color_service import ColorService
from krita_batch_export.Model.png_settings import PNGSettings


class PNGSettingsService:
    @staticmethod
    def to_dict(settings: PNGSettings):
        """Converts the PNGSettings Model to a dictionary"""
        return {
            "compression": settings.compression,
            "save_as_indexed": settings.save_as_indexed,
            "interlacing": settings.interlacing,
            "save_as_hdr": settings.save_as_hdr,
            "embed_srgb": settings.embed_srgb,
            "force_srgb": settings.force_srgb,
            "store_alpha": settings.store_alpha,
            "store_metadata": settings.store_metadata,
            "sign_with_author": settings.sign_with_author,
            "force_eight_bit": settings.force_eight_bit,
            "transparent_color_R": settings.transparent_color_R,
            "transparent_color_G": settings.transparent_color_G,
            "transparent_color_B": settings.transparent_color_B,
        }

    @staticmethod
    def from_dict(settings_dict):
        """Creates the PNGSettings Model from a dictionary"""
        return PNGSettings(**settings_dict)

    @staticmethod
    def to_info_object(settings: PNGSettings):
        """Converts the PNGSettings Model to an InfoObject() containing the user's chosen settings"""
        exportInfo = InfoObject()

        # Populate the InfoObject for PNG export
        exportInfo.setProperty("alpha", settings.store_alpha)
        exportInfo.setProperty("compression", settings.compression)
        exportInfo.setProperty("forceSRGB", settings.force_srgb)
        exportInfo.setProperty("indexed", settings.save_as_indexed)
        exportInfo.setProperty("interlaced", settings.interlacing)
        exportInfo.setProperty("saveAsHDR", settings.save_as_hdr)
        exportInfo.setProperty("saveSRGBProfile", settings.embed_srgb)
        exportInfo.setProperty("storeAuthor", settings.sign_with_author)
        exportInfo.setProperty("storeMetaData", settings.store_metadata)
        exportInfo.setProperty(
            "transparencyFillcolor",
            ColorService.RGB_to_krita_color_format(
                [settings.transparent_color_R, settings.transparent_color_G, settings.transparent_color_B]
            ),
        )

        return exportInfo