from krita import *
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
import os
import re

class BatchExportExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        # Create a new action in Krita's file menu that will trigger the batch export
        action = window.createAction("batch_export", "Batch Export", "file")
        action.setIcon(QIcon.fromTheme("document-export"))
        action.triggered.connect(self.batch_export)

    def batch_export(self):
        # Open a file dialogue to let the user choose a base filename and format
        file_name, file_ext = QFileDialog.getSaveFileName(
            None,
            "Select base filename and format",
            "",
            "PNG image (*.png);;JPEG image (*.jpg);;TIFF image (*.tif);;All Files (*)"
        )
        if not file_name:
            return  # User canceled


        # Get the base filename and extension
        base, ext = os.path.splitext(file_name)
        # If the file extension wasn't specified in the file name, try to determine it from the selected filter
        if not ext:
            match = re.search(r"\*\.(\w+)", file_ext) # Match the file extension in the filter, e.g. '*.png'
            if match:
                ext = '.' + match.group(1)  # extract the extension from the match, e.g. 'png'
            else:
                # If the file extension can't be determined from the filter, default to .png
                ext = '.png'


        # Get all currently open documents
        docs = Krita.instance().documents()
        if not docs:
            print("No documents open")
            return


        # Iterate through all open documents and export them
        for index, doc in enumerate(docs, start=1):
            # Create a unique filename for each file by appending it with an ascending number
            export_file_name = f"{base}_{index:03}{ext}"
            print(f"Exporting '{doc.name()}' to '{export_file_name}'...")

            # Ask for the export settings (e.g. compression level for PNG) only for the first document
            # Krita always uses the last used settings for subsequent exports

            # FIXME: This isn't best practice since it relies on my personal observations with Krita - it's not an officially documented Feature
            # FIXME: If this behavior changes in a future version of Krita, this code will break
            if index != 1:
                doc.setBatchmode(True)  # no popups while saving


            success = doc.exportImage(export_file_name, InfoObject())
            if not success:
                print(f"Failed to export '{doc.name()}'")

        print("Batch export completed!")


# Add the extension to Krita's list of extensions:
Krita.instance().addExtension(BatchExportExtension(Krita.instance()))