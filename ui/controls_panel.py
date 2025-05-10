"""
Control panel for the pendulum data analysis application.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, 
    QCheckBox
)
from PyQt5.QtCore import pyqtSignal


class ControlsPanel(QWidget):
    """
    Control panel for plot settings and analysis options.
    """
    
    # Define signals
    plotSettingsChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Initialize the controls panel.
        
        Args:
            parent (QWidget, optional): Parent widget
        """
        super().__init__(parent)
        
        # Store plot checkboxes
        self.plot_checkboxes = {}
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        main_layout = QVBoxLayout()
        
        # Create plot selection group
        plot_group = self._create_plot_selection_group()
        main_layout.addWidget(plot_group)
        
        # Add any additional controls (future)
        
        # Add stretch to push controls to the top
        main_layout.addStretch(1)
        
        self.setLayout(main_layout)
    
    def _create_plot_selection_group(self):
        """
        Create the plot selection group.
        
        Returns:
            QGroupBox: The plot selection group box
        """
        group_box = QGroupBox("Plot Selection")
        layout = QVBoxLayout()
        
        # Create checkboxes for each plot type
        from utils.config import Config
        for plot_id, plot_info in Config.PLOT_TYPES.items():
            checkbox = QCheckBox(plot_info['name'])
            checkbox.setChecked(plot_info['enabled_by_default'])
            checkbox.setToolTip(plot_info['description'])
            checkbox.stateChanged.connect(self._on_plot_selection_changed)
            
            layout.addWidget(checkbox)
            self.plot_checkboxes[plot_id] = checkbox
        
        group_box.setLayout(layout)
        return group_box
    

    
    def _on_plot_selection_changed(self):
        """Handle plot selection changes."""
        # Emit signal to notify of changes
        self.plotSettingsChanged.emit()
    
    def get_enabled_plots(self):
        """
        Get the currently enabled plots.
        
        Returns:
            dict: Dictionary of plot IDs and their enabled state
        """
        return {
            plot_id: checkbox.isChecked()
            for plot_id, checkbox in self.plot_checkboxes.items()
        }
    
    def update_from_plot_manager(self, plot_manager):
        """
        Update the UI from the plot manager state.
        
        Args:
            plot_manager: The plot manager to get state from
        """
        # Update plot checkboxes
        available_plots = plot_manager.get_available_plots()
        for plot_id, plot_info in available_plots.items():
            if plot_id in self.plot_checkboxes:
                self.plot_checkboxes[plot_id].setChecked(plot_info['enabled'])
