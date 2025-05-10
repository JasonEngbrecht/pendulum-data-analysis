"""
Plot panel for the pendulum data analysis application.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


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
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.no_data_label = QLabel("No data loaded. Select a file to begin.")
        self.no_data_label.setStyleSheet("QLabel { color: gray; font-size: 14px; }")
        self.no_data_label.setAlignment(Qt.AlignCenter)
        
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
        self.canvas.draw()
    
    def refresh(self):
        """Refresh the plot display."""
        self.canvas.draw()
