"""
Plot panel for the pendulum data analysis application.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class PlotPanel(QWidget):
    """
    Panel for displaying plots in the pendulum data analysis application.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the plot panel.
        
        Args:
            parent (QWidget, optional): Parent widget
        """
        super().__init__(parent)
        
        # Initialize attributes
        self.figure = Figure(figsize=(10, 12), dpi=100)  # Taller figure for vertical stacking
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.no_data_label = QLabel("No data loaded. Select a file to begin.")
        self.no_data_label.setStyleSheet("QLabel { color: gray; font-size: 14px; }")
        self.no_data_label.setAlignment(Qt.AlignCenter)
        
        # List to keep track of axes for synchronization
        self.axes_list = []
        
        # Initialize UI
        self._init_ui()
        
        # Connect to events for axis synchronization
        self.canvas.mpl_connect('draw_event', self._on_draw)
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        
        # Add matplotlib canvas and toolbar
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        # Initially show the no data label
        layout.addWidget(self.no_data_label)
        
        self.setLayout(layout)
        
        # Start with no data
        self.show_no_data(True)
    
    def show_no_data(self, show=True):
        """
        Show/hide the 'no data' message.
        
        Args:
            show (bool): Whether to show the message
        """
        self.no_data_label.setVisible(show)
        self.canvas.setVisible(not show)
        self.toolbar.setVisible(not show)
    
    def get_figure(self):
        """
        Get the figure for plotting.
        
        Returns:
            matplotlib.figure.Figure: The figure
        """
        return self.figure
    
    def clear_plots(self):
        """Clear all plots from the figure."""
        self.figure.clear()
        self.axes_list = []  # Clear the axes list
        self.canvas.draw()
    
    def refresh(self):
        """Refresh the plot display."""
        self.canvas.draw()
    
    def _on_draw(self, event):
        """Handle draw events for axis synchronization."""
        # Skip if no axes or only one axis
        if len(self.axes_list) <= 1:
            return
            
        # Find the current x limits of all axes
        x_limits = [ax.get_xlim() for ax in self.axes_list]
        
        # If there are differences in x limits, sync them to the most recently modified axis
        if not all(lim == x_limits[0] for lim in x_limits):
            # Find the axis that was most recently modified
            # For simplicity, we'll assume the last axis in the event's figure is the one being modified
            # This is not perfect but works for most interactions
            self._sync_x_axes()
    
    def _sync_x_axes(self):
        """Synchronize the x-axes of all plots."""
        if not self.axes_list:
            return
            
        # We'll use the first axis as the reference
        x_min, x_max = self.axes_list[0].get_xlim()
        
        # Set the same x limits on all axes
        for ax in self.axes_list:
            ax.set_xlim(x_min, x_max)
        
        # Redraw the canvas
        self.canvas.draw_idle()
    
    def register_axes(self, axes):
        """Register axes for synchronization."""
        self.axes_list = axes
        
        # Set up linked x-axes using matplotlib's callbacks
        if len(self.axes_list) > 1:
            # Make each axis sharex with the first one
            for ax in self.axes_list[1:]:
                ax.sharex(self.axes_list[0])
