"""
Main window for the pendulum data analysis application.
"""

import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QAction, QFileDialog, QMessageBox, QLabel, QStatusBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from ui.plot_panel import PlotPanel
from ui.controls_panel import ControlsPanel
from ui.file_selector import FileSelector
from core.data_loader import DataLoader
from core.plot_manager import PlotManager
from utils.plot_helpers import fix_bottom_axis_ticks


class MainWindow(QMainWindow):
    """
    Main window for the pendulum data analysis application.
    """
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Initialize components
        self.plot_panel = PlotPanel(self)
        self.controls_panel = ControlsPanel(self)
        self.data_loader = DataLoader()
        self.plot_manager = PlotManager()
        
        # Track current file
        self.current_file = None
        
        # Initialize UI
        self._init_ui()
        self._setup_connections()
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Set window properties
        self.setWindowTitle("Pendulum Data Analysis")
        self.setMinimumSize(1000, 800)  # Increased height for better plot display
        
        # Create central widget
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Create the plot panel (left side)
        main_layout.addWidget(self.plot_panel, 8)  # 80% of width
        
        # Create the controls panel (right side)
        main_layout.addWidget(self.controls_panel, 2)  # 20% of width
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Create menu bar
        self._create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _create_menu_bar(self):
        """Create the menu bar."""
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        
        # Open action
        open_action = QAction("&Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open a pendulum data file")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = self.menuBar().addMenu("&View")
        
        # Reset view action
        reset_view_action = QAction("&Reset View", self)
        reset_view_action.setStatusTip("Reset the plot view")
        reset_view_action.triggered.connect(self._reset_view)
        view_menu.addAction(reset_view_action)
        
        # Analysis menu (for future use)
        analysis_menu = self.menuBar().addMenu("&Analysis")
        
        # Placeholder for future analysis actions
        analysis_action = QAction("&Coming Soon...", self)
        analysis_action.setEnabled(False)
        analysis_menu.addAction(analysis_action)
        
        # Help menu
        help_menu = self.menuBar().addMenu("&Help")
        
        # About action
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_connections(self):
        """Set up signal-slot connections."""
        # Connect control panel signals
        self.controls_panel.plotSettingsChanged.connect(self._on_plot_settings_changed)
    
    def open_file(self):
        """Open a pendulum data file."""
        file_path = FileSelector.get_csv_file(self)
        if file_path:
            self._load_data(file_path)
    
    def _load_data(self, file_path):
        """
        Load data from a file.
        
        Args:
            file_path (str): Path to the data file
        """
        # Update status
        self.status_bar.showMessage(f"Loading {os.path.basename(file_path)}...")
        
        # Load the data
        if self.data_loader.load_csv(file_path):
            # Update current file
            self.current_file = file_path
            
            # Show the plots
            self.plot_panel.show_no_data(False)
            
            # Update the plots
            self._update_plots()
            
            # Update status
            self.status_bar.showMessage(f"Loaded {os.path.basename(file_path)}")
        else:
            # Show error message
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load {os.path.basename(file_path)}",
                QMessageBox.Ok
            )
            
            # Update status
            self.status_bar.showMessage("Error loading file")
    
    def _update_plots(self):
        """Update the plots based on current settings."""
        if not self.data_loader.is_loaded:
            print("No data loaded, cannot update plots")
            return
        
        print("Updating plots...")
        
        # Get the data
        data = self.data_loader.get_data()
        print(f"Data for plotting: {data.shape} rows, {data.columns.tolist()}")
        
        # Update the plot manager with current UI settings
        enabled_plots = self.controls_panel.get_enabled_plots()
        print(f"Enabled plots: {enabled_plots}")
        
        for plot_id, enabled in enabled_plots.items():
            self.plot_manager.set_plot_enabled(plot_id, enabled)
        
        # Create the plots
        figure = self.plot_panel.get_figure()
        created_plots, all_axes = self.plot_manager.create_plots(data, figure)
        print(f"Created {len(created_plots)} plots")
        
        # Register axes for synchronization
        self.plot_panel.register_axes(all_axes)
        
        # Force tick labels to appear on bottom plot
        fix_bottom_axis_ticks(all_axes)
        
        # Refresh the display
        self.plot_panel.refresh()
        print("Plots refreshed")
    
    def _on_plot_settings_changed(self):
        """Handle plot settings changes."""
        self._update_plots()
    

    
    def _reset_view(self):
        """Reset the plot view."""
        # Update the plots with auto scaling
        self._update_plots()
    
    def _show_about(self):
        """Show the about dialog."""
        QMessageBox.about(
            self,
            "About Pendulum Data Analysis",
            "<h3>Pendulum Data Analysis</h3>"
            "<p>Version 0.1.0</p>"
            "<p>A tool for analyzing pendulum motion data.</p>"
        )
