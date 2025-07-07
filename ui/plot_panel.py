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
        self.figure = Figure(figsize=(10, 14), dpi=100)  # Taller figure for vertical stacking, more height for more compact plots
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.no_data_label = QLabel("No data loaded. Select a file to begin.")
        self.no_data_label.setStyleSheet("QLabel { color: gray; font-size: 14px; }")
        self.no_data_label.setAlignment(Qt.AlignCenter)
        
        # Label for when all data is filtered out
        self.no_data_after_filter_label = QLabel("All data points have been filtered out. Adjust filter settings to see data.")
        self.no_data_after_filter_label.setStyleSheet("QLabel { color: orange; font-size: 14px; }")
        self.no_data_after_filter_label.setAlignment(Qt.AlignCenter)
        self.no_data_after_filter_label.setVisible(False)
        
        # List to keep track of axes for synchronization
        self.axes_list = []
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        
        # Add matplotlib canvas and toolbar
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        # Initially show the no data label
        layout.addWidget(self.no_data_label)
        layout.addWidget(self.no_data_after_filter_label)
        
        self.setLayout(layout)
        
        # Start with no data
        self.show_no_data(True)
    
    def show_no_data(self, show=True, filtered=False):
        """
        Show/hide the 'no data' message.
        
        Args:
            show (bool): Whether to show the message
            filtered (bool): Whether this is due to filtering
        """
        if show:
            # Clear any existing plots when showing no data message
            self.clear_plots()
            # Show appropriate message
            self.no_data_label.setVisible(not filtered)
            self.no_data_after_filter_label.setVisible(filtered)
            self.canvas.setVisible(False)
            self.toolbar.setVisible(False)
        else:
            # Hide all messages and show plots
            self.no_data_label.setVisible(False)
            self.no_data_after_filter_label.setVisible(False)
            self.canvas.setVisible(True)
            self.toolbar.setVisible(True)
            # Force a refresh to ensure canvas is updated
            self.canvas.draw_idle()
    
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
    
    def register_axes(self, axes):
        """Register axes for synchronization."""
        self.axes_list = axes
