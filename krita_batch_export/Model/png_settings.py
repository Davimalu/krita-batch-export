class PNGSettings:
    """Class to hold the settings for the PNG export as chosen by the user"""
    def __init__(self, compression=3, save_as_indexed=False, interlacing=False, save_as_hdr=False,
                 embed_srgb=True, force_srgb=False, store_alpha=False, store_metadata=False,
                 sign_with_author=False, force_eight_bit=False, transparent_color_R=0,
                 transparent_color_G=0, transparent_color_B=0):
        self.compression = compression
        self.save_as_indexed = save_as_indexed
        self.interlacing = interlacing
        self.save_as_hdr = save_as_hdr
        self.embed_srgb = embed_srgb
        self.force_srgb = force_srgb
        self.store_alpha = store_alpha
        self.store_metadata = store_metadata
        self.sign_with_author = sign_with_author
        self.force_eight_bit = force_eight_bit
        self.transparent_color_R = transparent_color_R
        self.transparent_color_G = transparent_color_G
        self.transparent_color_B = transparent_color_B