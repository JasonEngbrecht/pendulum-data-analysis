"""
Base class for all plot types in the pendulum data analysis application.
"""

import matplotlib.pyplot as plt


class BasePlot:
    """
    Base class for all plot types.
    Provides common functionality for all plots.
    """
    
    def __init__(self, data, ax, title=""):
        """
        Initialize the base plot.
        
        Args:
            data (pandas.DataFrame): Data to plot
            ax (matplotlib.axes.Axes): Matplotlib axes to plot on
            title (str, optional): Plot title
        """
        self.data = data
        self.ax = ax
        self.title = title
        self.is_initialized = False
        
        # Default axis limits (None means auto)
        self.axis_limits = {
            'x_min': None,
            'x_max': None,
            'y_min': None,
            'y_max': None
        }
    
    def initialize(self):
        """
        Initialize the plot.
        This method should be called once before updating the plot.
        
        Returns:
            bool: True if successful, False otherwise
        """
        # This method should be overridden by subclasses
        self.is_initialized = True
        return True
    
    def update(self):
        """
        Update the plot with the current data.
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Initialize if not already done
        if not self.is_initialized:
            self.initialize()
        
        # Apply axis limits
        self._apply_axis_limits()
        
        # Redraw the plot
        if hasattr(self.ax.figure.canvas, 'draw_idle'):
            self.ax.figure.canvas.draw_idle()
        
        return True
    
    def update_axis_limits(self, limits):
        """
        Update the axis limits for this plot.
        
        Args:
            limits (dict): Dictionary containing x_min, x_max, y_min, y_max
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Update only the provided limits
        for key in ['x_min', 'x_max', 'y_min', 'y_max']:
            if key in limits and limits[key] is not None:
                self.axis_limits[key] = limits[key]
        
        # Apply the new limits
        self._apply_axis_limits()
        
        return True
    
    def _apply_axis_limits(self):
        """
        Apply the current axis limits to the plot.
        """
        if self.ax is None:
            return
        
        # Get current limits for any that are set to auto (None)
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()
        
        # Apply limits, using current limits for any that are None
        self.ax.set_xlim(
            self.axis_limits['x_min'] if self.axis_limits['x_min'] is not None else x_min,
            self.axis_limits['x_max'] if self.axis_limits['x_max'] is not None else x_max
        )
        
        self.ax.set_ylim(
            self.axis_limits['y_min'] if self.axis_limits['y_min'] is not None else y_min,
            self.axis_limits['y_max'] if self.axis_limits['y_max'] is not None else y_max
        )
    
    def clear(self):
        """
        Clear the plot.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.ax is not None:
            self.ax.clear()
            # Don't set title to keep plots compact
            return True
        return False
