"""
Control panel for the pendulum data analysis application.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QCheckBox, QLabel, QDoubleSpinBox, QPushButton,
    QFormLayout
)
from PyQt5.QtCore import pyqtSignal


class ControlsPanel(QWidget):
    """
    Control panel for plot settings and analysis options.
    """
    
    # Define signals
    plotSettingsChanged = pyqtSignal()
    axisLimitsChanged = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        """
        Initialize the controls panel.
        
        Args:
            parent (QWidget, optional): Parent widget
        """
        super().__init__(parent)
        
        # Store plot checkboxes and axis limit controls
        self.plot_checkboxes = {}
        self.axis_limits = {}
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        main_layout = QVBoxLayout()
        
        # Create plot selection group
        plot_group = self._create_plot_selection_group()
        main_layout.addWidget(plot_group)
        
        # Create axis limits group
        axis_group = self._create_axis_limits_group()
        main_layout.addWidget(axis_group)
        
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
    
    def _create_axis_limits_group(self):
        """
        Create the axis limits group.
        
        Returns:
            QGroupBox: The axis limits group box
        """
        group_box = QGroupBox("Axis Limits")
        layout = QFormLayout()
        
        # Create spinboxes for each axis limit
        self.axis_limits['x_min'] = self._create_spinbox(-10000, 10000, 0.1, None)
        self.axis_limits['x_max'] = self._create_spinbox(-10000, 10000, 0.1, None)
        self.axis_limits['y_min'] = self._create_spinbox(-10000, 10000, 0.1, None)
        self.axis_limits['y_max'] = self._create_spinbox(-10000, 10000, 0.1, None)
        
        # Add spinboxes to layout
        layout.addRow("X Min:", self.axis_limits['x_min'])
        layout.addRow("X Max:", self.axis_limits['x_max'])
        layout.addRow("Y Min:", self.axis_limits['y_min'])
        layout.addRow("Y Max:", self.axis_limits['y_max'])
        
        # Add buttons to set/reset limits
        btn_layout = QHBoxLayout()
        
        # Apply button
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self._on_apply_limits)
        
        # Auto button (reset to auto)
        auto_btn = QPushButton("Auto")
        auto_btn.clicked.connect(self._on_auto_limits)
        
        btn_layout.addWidget(apply_btn)
        btn_layout.addWidget(auto_btn)
        
        layout.addRow("", btn_layout)
        
        group_box.setLayout(layout)
        return group_box
    
    def _create_spinbox(self, min_val, max_val, step, default_val):
        """
        Create a spinbox for axis limits.
        
        Args:
            min_val (float): Minimum value
            max_val (float): Maximum value
            step (float): Step size
            default_val (float, optional): Default value
            
        Returns:
            QDoubleSpinBox: The created spinbox
        """
        spinbox = QDoubleSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setSingleStep(step)
        spinbox.setDecimals(2)
        spinbox.setSpecialValueText("Auto")  # Display "Auto" for minimum value
        
        # Set to special value by default (meaning auto)
        if default_val is None:
            spinbox.setValue(min_val)
        else:
            spinbox.setValue(default_val)
        
        return spinbox
    
    def _on_plot_selection_changed(self):
        """Handle plot selection changes."""
        # Emit signal to notify of changes
        self.plotSettingsChanged.emit()
    
    def _on_apply_limits(self):
        """Handle apply limits button click."""
        limits = {}
        
        # Collect limit values from spinboxes, using None for "Auto"
        for key, spinbox in self.axis_limits.items():
            value = spinbox.value()
            if spinbox.specialValueText() and value == spinbox.minimum():
                # This is the special "Auto" value
                limits[key] = None
            else:
                limits[key] = value
        
        # Emit signal with the new limits
        self.axisLimitsChanged.emit(limits)
    
    def _on_auto_limits(self):
        """Handle auto limits button click."""
        # Reset all spinboxes to "Auto"
        for spinbox in self.axis_limits.values():
            spinbox.setValue(spinbox.minimum())
        
        # Emit signal with all auto limits
        self.axisLimitsChanged.emit({
            'x_min': None,
            'x_max': None,
            'y_min': None,
            'y_max': None
        })
    
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
        
        # Update axis limits
        axis_limits = plot_manager.get_axis_limits()
        for key, value in axis_limits.items():
            if key in self.axis_limits:
                if value is None:
                    # Set to "Auto"
                    self.axis_limits[key].setValue(self.axis_limits[key].minimum())
                else:
                    self.axis_limits[key].setValue(value)
