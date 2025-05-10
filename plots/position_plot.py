"""
Position plot for pendulum analysis.
Displays an X-Y scatter plot of pendulum position.
"""

import numpy as np
from plots.base_plot import BasePlot


class PositionPlot(BasePlot):
    """
    Position plot showing X-Y coordinates of the pendulum.
    """
    
    def __init__(self, data, ax):
        """
        Initialize the position plot.
        
        Args:
            data (pandas.DataFrame): Data to plot
            ax (matplotlib.axes.Axes): Matplotlib axes to plot on
        """
        super().__init__(data, ax, title="Pendulum Position")
        
        # Store plot elements
        self.scatter = None
        
        # Find the appropriate column names
        self.x_col = self._find_column('x')
        self.y_col = self._find_column('y')
    
    def _find_column(self, dimension):
        """
        Find the appropriate column name for a given dimension.
        
        Args:
            dimension (str): The dimension to find ('x' or 'y')
            
        Returns:
            str: The column name, or None if not found
        """
        if dimension not in ['x', 'y']:
            return None
            
        # Try various possible column names
        possible_names = [
            dimension,
            f"{dimension}_pos",
            f"{dimension} position",
            f"{dimension}-position",
            f"{dimension}_position"
        ]
        
        # Check if any of the possible names exist in the data
        for name in possible_names:
            if name in self.data.columns:
                return name
                
        # If no exact match, try case-insensitive matching
        for col in self.data.columns:
            col_lower = col.lower()
            if any(name.lower() in col_lower for name in possible_names):
                return col
                
        return None
    
    def initialize(self):
        """
        Initialize the position plot.
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Make sure we have valid column names
        if self.x_col is None or self.y_col is None:
            print("Error: Could not find appropriate X and Y columns in the data")
            return False
        
        # Set up the axes
        self.ax.set_xlabel(f"{self.x_col} Position")
        self.ax.set_ylabel(f"{self.y_col} Position")
        self.ax.set_title("Pendulum Position")
        self.ax.grid(True)
        
        # Create the scatter plot
        self.scatter = self.ax.scatter(
            self.data[self.x_col],
            self.data[self.y_col],
            s=10,  # Marker size
            c=np.arange(len(self.data)),  # Color by time
            cmap='viridis',
            alpha=0.7
        )
        
        # Add a colorbar as a time indicator
        cbar = self.ax.figure.colorbar(self.scatter, ax=self.ax)
        cbar.set_label('Time Index')
        
        # Set aspect ratio to equal for true representation of distances
        self.ax.set_aspect('equal')
        
        self.is_initialized = True
        return True
    
    def update(self):
        """
        Update the position plot with the current data.
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if we need to initialize first
        if not self.is_initialized:
            if not self.initialize():
                return False
        
        # Update the scatter plot with new data
        if self.scatter is not None:
            self.scatter.set_offsets(np.column_stack([
                self.data[self.x_col],
                self.data[self.y_col]
            ]))
            
            # Update the color mapping for time
            self.scatter.set_array(np.arange(len(self.data)))
        
        # Apply axis limits and refresh
        super().update()
        
        return True
