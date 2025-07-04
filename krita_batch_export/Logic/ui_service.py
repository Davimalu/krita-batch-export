from krita_batch_export.Config.config_service import ConfigService
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog

@staticmethod
def get_file_path():
    """
    Opens a file dialog to let the user choose a base filename and format and returns the full path to the selected file including the file extension
    """

    # Get the supported file formats from the config
    supported_file_formats = ConfigService.get_file_formats()
    file_filter = ";;".join(
        [f'{fmt["name"]} (*.{fmt["extension"]})' for fmt in supported_file_formats]
        # -> 'PNG image (*.png);;JPEG image (*.jpg);;TIFF image (*.tif)';;...
    )

    # Open a file dialog to let the user choose a base filename and format
    file_name, file_ext = QFileDialog.getSaveFileName(
        None,
        "Select base filename and format",
        "",
        file_filter
    )
    if not file_name:
        return  # User canceled

    # Get the base filename and extension
    base, ext = os.path.splitext(file_name)
    # If the file extension wasn't specified in the file name, try to determine it from the selected filter
    if not ext:
        match = re.search(r"\*\.(\w+)", file_ext)  # Match the file extension in the filter, e.g. '*.png'
        if match:
            ext = '.' + match.group(1)  # extract the extension from the match, e.g. 'png'
        else:
            # If the file extension can't be determined from the filter, default to .png
            ext = '.png'

    return base, ext