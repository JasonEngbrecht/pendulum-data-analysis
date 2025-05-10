"""
Pendulum Data Analysis

A tool for visualizing and analyzing pendulum motion data.
The application allows loading CSV files containing pendulum position data,
viewing various plots of the data, and performing analysis on the data.
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Main entry point for the application."""
    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("Pendulum Data Analysis")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
