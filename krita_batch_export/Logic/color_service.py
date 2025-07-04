import xml.etree.ElementTree as ET

class ColorService:
    def __init__(self):
        pass

    @staticmethod
    def RGB_to_krita_color_format(rgb):
        """
        Converts RGB values to the XML format required by Krita for color representation.

        Args:
            rgb (list): A list containing RGB values, e.g., [R, G, B] where each value is between 0 and 255.

        Returns:
            str: An XML string representing the color in Krita's required format (used for the transparencyFillcolor parameter).
        """

        # TODO: This implementation is not correct
        r, g, b = [channel / 255.0 for channel in rgb]  # Normalize to 0-1 range

        color_element = ET.Element("color")
        ET.SubElement(color_element, "RGB", {
            "r": str(r),
            "g": str(g),
            "b": str(b),
            "space": "sRGB-elle-V2-srgbtrc.icc"
        })

        # Convert to XML string
        return ET.tostring(color_element, encoding="unicode")

