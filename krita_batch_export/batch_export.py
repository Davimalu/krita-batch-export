import os
import re
import time

from krita import *
from PyQt5.QtWidgets import QFileDialog, QProgressDialog, QMessageBox, QDialog, QLabel, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Import custom dialogs for supported file formats
from krita_batch_export.ExportDialogs.png_export_dialog import PNGExportDialog

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


        # Open a file dialog to let the user choose a base filename and format
        file_name, file_ext = QFileDialog.getSaveFileName(
            None,
            "Select base filename and format",
            "",
            "PNG image (*.png);;JPEG image (*.jpg);;TIFF image (*.tif)"
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


        # Open the appropriate export dialog based on the selected file format (for the selection of compression level, etc.)
        exportInfo = InfoObject()
        if ext.lower() == '.png':
            dialog = PNGExportDialog()
            if dialog.exec_() == QDialog.Rejected:
                return  # User canceled the settings dialog

            exportInfo = dialog.getInfoObject()

        elif ext.lower() in ('.jpg', '.jpeg'):
            # Similar logic for JPEG using a custom JPEG dialog
            # dialog = JPEGExportDialog()
            # if dialog.exec_() == QDialog.Rejected:
            #     return
            # settings = dialog.getSettings()
            # info.setProperty("quality", settings["quality"])
            pass
        elif ext.lower() == '.tif':
            # And for TIFF...
            pass
        else:
            # You might want to restrict unsupported formats.
            QMessageBox.warning(None, "Unsupported format", "This file format is not supported for batch export.")
            return


        # Prepare a progress dialog
        progress_dialog = QProgressDialog("Starting export...", "Cancel", 0, len(docs))
        progress_dialog.setWindowTitle("Batch Export")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        # Start timer to measure the time taken for the export
        start_time = time.time()
        elapsed_time = 0
        estimated_time_remaining = 0

        # Iterate through all open documents and export them
        for index, doc in enumerate(docs, start=1):
            # Abort the export if the user clicked "Cancel" in the progress dialog
            if progress_dialog.wasCanceled():
                break

            # Create a unique filename for each file by appending it with an ascending number
            export_file_name = f"{base}_{index:03}{ext}"

            # Update the progress dialog
            progress_dialog.setLabelText(
                f"Exporting {index} of {len(docs)}: {export_file_name}\n"
                f"\n"
                f"Elapsed Time: {elapsed_time:.2f} s\n"
                f"Remaining Time: {estimated_time_remaining:.2f} s"
            )
            progress_dialog.setValue(index - 1)  # -1 because the index is of the progress bar is 0-based

            # Process GUI events | If this isn't done, the export loop monopolizes the main thread and the GUI can't render properly
            QApplication.processEvents()

            # Export the document with the specified settings
            doc.setBatchmode(True)  # disable popups while saving
            success = doc.exportImage(export_file_name, exportInfo)
            if not success:
                print(f"Failed to export '{doc.name()}'")

            doc.setBatchmode(False)  # re-enable popups

            # Calculate elapsed time
            elapsed_time = time.time() - start_time
            # Calculate estimated time remaining based on the progress so far
            estimated_time_remaining = (elapsed_time / index) * (len(docs) - index)

        # Complete the progress dialog and close it
        progress_dialog.setValue(len(docs))
        progress_dialog.close()

        if not progress_dialog.wasCanceled():
            QMessageBox.information(None, "Batch Export", "Export completed successfully!")


# Add the extension to Krita's list of extensions:
Krita.instance().addExtension(BatchExportExtension(Krita.instance()))