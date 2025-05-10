"""
Time series plot for pendulum analysis.
Displays a time series of pendulum position in X or Y dimension.
"""

from plots.base_plot import BasePlot


class TimeSeriesPlot(BasePlot):
    """
    Time series plot showing pendulum position over time.
    """
    
    def __init__(self, data, ax, dimension='x'):
        """
        Initialize the time series plot.
        
        Args:
            data (pandas.DataFrame): Data to plot
            ax (matplotlib.axes.Axes): Matplotlib axes to plot on
            dimension (str, optional): Dimension to plot ('x' or 'y')
        """
        title = f"{dimension.upper()} Position Over Time"
        super().__init__(data, ax, title=title)
        
        # Store plot elements
        self.line = None
        self.dimension = dimension
        
        # Find the appropriate column names
        self.time_col = self._find_time_column()
        self.pos_col = self._find_position_column(dimension)
    
    def _find_time_column(self):
        """
        Find the appropriate column name for time.
        
        Returns:
            str: The column name, or None if not found
        """
        # Try various possible column names
        possible_names = ['time', 't', 'timestamp', 'time_stamp']
        
        # Check if any of the possible names exist in the data
        for name in possible_names:
            if name in self.data.columns:
                return name
                
        # If no exact match, try case-insensitive matching
        for col in self.data.columns:
            col_lower = col.lower()
            if any(name.lower() in col_lower for name in possible_names):
                return col
                
        # If we still haven't found a time column, use the index as a fallback
        return None
    
    def _find_position_column(self, dimension):
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
        Initialize the time series plot.
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Make sure we have valid column names
        if self.pos_col is None:
            print(f"Error: Could not find appropriate {self.dimension.upper()} position column in the data")
            return False
        
        # Set up the axes
        if self.time_col:
            self.ax.set_xlabel("Time")
            x_data = self.data[self.time_col]
        else:
            self.ax.set_xlabel("Sample Index")
            x_data = self.data.index
            
        self.ax.set_ylabel(f"{self.dimension.upper()} Position")
        self.ax.set_title(f"{self.dimension.upper()} Position Over Time")
        self.ax.grid(True)
        
        # Create the line plot
        self.line, = self.ax.plot(
            x_data,
            self.data[self.pos_col],
            'b-',  # Blue line
            linewidth=1.5,
            alpha=0.8
        )
        
        # Add markers to show individual data points
        self.markers = self.ax.scatter(
            x_data,
            self.data[self.pos_col],
            s=20,  # Marker size
            color='red',
            alpha=0.5
        )
        
        self.is_initialized = True
        return True
    
    def update(self):
        """
        Update the time series plot with the current data.
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if we need to initialize first
        if not self.is_initialized:
            if not self.initialize():
                return False
        
        # Update the line and markers with new data
        if self.time_col:
            x_data = self.data[self.time_col]
        else:
            x_data = self.data.index
            
        if self.line is not None:
            self.line.set_xdata(x_data)
            self.line.set_ydata(self.data[self.pos_col])
            
        if self.markers is not None:
            self.markers.set_offsets(list(zip(x_data, self.data[self.pos_col])))
        
        # Apply axis limits and refresh
        super().update()
        
        return True
