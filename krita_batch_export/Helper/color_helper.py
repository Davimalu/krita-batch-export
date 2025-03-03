import xml.etree.ElementTree as ET

def RGB_to_krita_color_format(rgb):
    """
    Takes a list containing an RGB color like [R, G, B] (values between 0 and 255)
    and generates the required XML string for Krita's transparencyFillcolor parameter.
    """
    # FIXME: Incompatible color spaces cause the color to be displayed incorrectly in the exported image

    r, g, b = [channel / 255.0 for channel in rgb]  # Normalize to 0-1 range

    color_element = ET.Element("color")
    ET.SubElement(color_element, "RGB", {
        "r": str(r),
        "g": str(g),
        "b": str(b),
        "space": "sRGB-elle-V2-srgbtrc.icc"
    })

    # Convert to XML string without additional CDATA wrapping
    return ET.tostring(color_element, encoding="unicode")

