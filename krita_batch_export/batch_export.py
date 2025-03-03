import os
import re

from krita import *
from PyQt5.QtWidgets import QFileDialog, QProgressDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

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
        # Get all currently open documents
        docs = Krita.instance().documents()
        if not docs:
            QMessageBox.information(None, "Batch Export", "No documents open")
            return


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


        # Prepare a progress dialog
        progress_dialog = QProgressDialog("Starting export...", "Cancel", 0, len(docs))
        progress_dialog.setWindowTitle("Batch Export")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()


        # Iterate through all open documents and export them
        for index, doc in enumerate(docs, start=1):
            # Abort the export if the user clicked "Cancel" in the progress dialog
            if progress_dialog.wasCanceled():
                break

            # Create a unique filename for each file by appending it with an ascending number
            export_file_name = f"{base}_{index:03}{ext}"

            # Update the progress dialog
            progress_dialog.setLabelText(f"Exporting {index} of {len(docs)}: {export_file_name}")
            progress_dialog.setValue(index - 1)  # -1 because the index is of the progress bar is 0-based

            # Ask for the export settings (e.g. compression level for PNG) only for the first document
            # Krita always uses the last used settings for subsequent exports

            # FIXME: This isn't best practice since it relies on my personal observations with Krita - it's not an officially documented Feature
            # FIXME: If this behavior changes in a future version of Krita, this code will break
            if index != 1:
                doc.setBatchmode(True)  # no popups while saving


            success = doc.exportImage(export_file_name, InfoObject())
            if not success:
                print(f"Failed to export '{doc.name()}'")

        # Complete the progress dialog and close it
        progress_dialog.setValue(len(docs))
        progress_dialog.close()

        if not progress_dialog.wasCanceled():
            QMessageBox.information(None, "Batch Export", "Export completed successfully!")


# Add the extension to Krita's list of extensions:
Krita.instance().addExtension(BatchExportExtension(Krita.instance()))