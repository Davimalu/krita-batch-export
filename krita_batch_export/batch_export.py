import time

from krita import *
from PyQt5.QtWidgets import QFileDialog, QProgressDialog, QMessageBox, QDialog, QLabel, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Import custom dialogs for supported file formats
from krita_batch_export.Logic.krita_service import KritaService
from krita_batch_export.Logic.file_service import FileService

class BatchExportExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        # Create a new action in Krita's file menu that will trigger the batch export
        action = window.createAction("batch_export", "Batch Export", "tools/scripts")
        action.setIcon(QIcon.fromTheme("document-export"))
        action.triggered.connect(self.batch_export)

    def batch_export(self):
        # Get a list of all open documents in Krita
        docs = KritaService.get_all_open_documents()
        if not docs:
            QMessageBox.information(None, "Batch Export", "No documents open")
            return

        # Ask the user where to save the files, get the base filename (full file path) and extension
        base, ext = FileService.get_file_path()

        # Open the appropriate export dialog based on the selected file format (for the selection of compression level, etc.)
        exportInfo = FileService.create_export_info(ext)
        if not exportInfo:
            return  # user canceled or unsupported format

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