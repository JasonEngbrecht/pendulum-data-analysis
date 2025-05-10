"""
File selector dialog for the pendulum data analysis application.
"""

from PyQt5.QtWidgets import (QFileDialog, QWidget)


class FileSelector:
    """
    Handles file selection for the pendulum data analysis application.
    """
    
    @staticmethod
    def get_csv_file(parent_widget: QWidget = None):
        """
        Open a file dialog to select a CSV file.
        
        Args:
            parent_widget (QWidget, optional): Parent widget for the dialog
            
        Returns:
            str: Selected file path, or None if no file was selected
        """
        import os
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        
        # Default to the data directory if it exists
        default_dir = ""
        data_dir = os.path.join(os.getcwd(), "data")
        if os.path.exists(data_dir) and os.path.isdir(data_dir):
            default_dir = data_dir
        
        file_path, _ = QFileDialog.getOpenFileName(
            parent_widget,
            "Open Pendulum Data File",
            default_dir,
            "CSV Files (*.csv);;All Files (*)",
            options=options
        )
        
        if file_path:
            return file_path
        
        return None
