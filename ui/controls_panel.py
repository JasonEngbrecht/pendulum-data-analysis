"""
Control panel for the pendulum data analysis application.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QHBoxLayout,
    QCheckBox, QLabel, QLineEdit, QPushButton
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QDoubleValidator, QFont


class ControlsPanel(QWidget):
    """
    Control panel for plot settings and analysis options.
    """
    
    # Define signals
    plotSettingsChanged = pyqtSignal()
    filterSettingsChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Initialize the controls panel.
        
        Args:
            parent (QWidget, optional): Parent widget
        """
        super().__init__(parent)
        
        # Store plot checkboxes
        self.plot_checkboxes = {}
        
        # Store filter controls
        self.filter_controls = {}
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        main_layout = QVBoxLayout()
        
        # Create plot selection group
        plot_group = self._create_plot_selection_group()
        main_layout.addWidget(plot_group)
        
        # Create filter controls group
        filter_group = self._create_filter_controls_group()
        main_layout.addWidget(filter_group)
        
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
    
    def _create_filter_controls_group(self):
        """
        Create the filter controls group.
        
        Returns:
            QGroupBox: The filter controls group box
        """
        group_box = QGroupBox("Data Filters")
        layout = QVBoxLayout()
        
        # Add filter controls for semi-major and semi-minor axes
        for axis_name, axis_label in [
            ('semi_major_axis', 'Semi-Major Axis'),
            ('semi_minor_axis', 'Semi-Minor Axis')
        ]:
            # Create horizontal layout for this filter
            filter_layout = QHBoxLayout()
            
            # Checkbox to enable/disable filter
            checkbox = QCheckBox(axis_label)
            checkbox.setChecked(False)  # Off by default
            checkbox.stateChanged.connect(self._on_filter_changed)
            filter_layout.addWidget(checkbox)
            
            # Min value input
            filter_layout.addWidget(QLabel("Min:"))
            min_input = QLineEdit()
            min_input.setFixedWidth(85)  # Width to accommodate ~7 digits + decimal point + 2 decimals
            # Set a monospace font for better number alignment
            font = QFont("Consolas")
            font.setPointSize(9)
            min_input.setFont(font)
            # Set validator without decimal restriction to allow proper input
            min_validator = QDoubleValidator()
            min_input.setValidator(min_validator)
            min_input.editingFinished.connect(self._on_filter_changed)
            filter_layout.addWidget(min_input)
            
            # Max value input
            filter_layout.addWidget(QLabel("Max:"))
            max_input = QLineEdit()
            max_input.setFixedWidth(85)  # Width to accommodate ~7 digits + decimal point + 2 decimals
            max_input.setFont(font)  # Same font as min input
            # Set validator without decimal restriction to allow proper input
            max_validator = QDoubleValidator()
            max_input.setValidator(max_validator)
            max_input.editingFinished.connect(self._on_filter_changed)
            filter_layout.addWidget(max_input)
            
            # Reset button
            reset_btn = QPushButton("IQR")
            reset_btn.setMaximumWidth(40)
            reset_btn.setToolTip("Reset to IQR bounds")
            reset_btn.clicked.connect(lambda checked, axis=axis_name: self._reset_filter_bounds(axis))
            filter_layout.addWidget(reset_btn)
            
            # Add stretch to push everything to the left
            filter_layout.addStretch()
            
            # Store references to controls
            self.filter_controls[axis_name] = {
                'checkbox': checkbox,
                'min_input': min_input,
                'max_input': max_input,
                'reset_btn': reset_btn
            }
            
            # Add to main layout
            layout.addLayout(filter_layout)
        
        # Add filter stats label
        self.filter_stats_label = QLabel("All data points shown")
        layout.addWidget(self.filter_stats_label)
        
        group_box.setLayout(layout)
        return group_box
    
    def _on_plot_selection_changed(self):
        """Handle plot selection changes."""
        # Emit signal to notify of changes
        self.plotSettingsChanged.emit()
    
    def _on_filter_changed(self):
        """Handle filter setting changes when editing is finished."""
        # Emit signal to notify of changes
        self.filterSettingsChanged.emit()
    

    def _reset_filter_bounds(self, axis_name):
        """Reset filter bounds to IQR values."""
        # Signal that we want to reset to IQR bounds
        # The MainWindow will handle this by checking for empty values
        if axis_name in self.filter_controls:
            # Clear the inputs to signal a reset
            self.filter_controls[axis_name]['min_input'].clear()
            self.filter_controls[axis_name]['max_input'].clear()
        self.filterSettingsChanged.emit()
    
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
    
    def get_filter_settings(self):
        """
        Get the current filter settings from the UI.
        
        Returns:
            dict: Filter settings for each axis
        """
        settings = {}
        for axis_name, controls in self.filter_controls.items():
            enabled = controls['checkbox'].isChecked()
            min_text = controls['min_input'].text()
            max_text = controls['max_input'].text()
            
            settings[axis_name] = {
                'enabled': enabled,
                'min': float(min_text) if min_text else None,
                'max': float(max_text) if max_text else None
            }
        return settings
    
    def update_filter_controls(self, filter_settings):
        """
        Update the filter controls from filter settings.
        
        Args:
            filter_settings (dict): Filter settings from FilterManager
        """
        for axis_name, settings in filter_settings.items():
            if axis_name in self.filter_controls:
                controls = self.filter_controls[axis_name]
                
                # Update checkbox
                controls['checkbox'].setChecked(settings.get('enabled', False))
                
                # Update min/max inputs
                min_val = settings.get('min')
                max_val = settings.get('max')
                
                if min_val is not None:
                    controls['min_input'].setText(f"{min_val:.2f}")
                if max_val is not None:
                    controls['max_input'].setText(f"{max_val:.2f}")
    
    def update_filter_stats(self, stats):
        """
        Update the filter statistics display.
        
        Args:
            stats (dict): Filter statistics from FilterManager
        """
        if stats['removed_count'] > 0:
            self.filter_stats_label.setText(
                f"Showing {stats['filtered_count']} of {stats['original_count']} points "
                f"({stats['removed_count']} filtered out)"
            )
        else:
            self.filter_stats_label.setText("All data points shown")
    
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
