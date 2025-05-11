"""
Time series plot for pendulum analysis.
Displays a time series of pendulum parameters over time.
"""

from plots.base_plot import BasePlot


class TimeSeriesPlot(BasePlot):
    """
    Time series plot showing a pendulum parameter over time.
    """
    
    def __init__(self, data, ax, parameter):
        """
        Initialize the time series plot.
        
        Args:
            data (pandas.DataFrame): Data to plot
            ax (matplotlib.axes.Axes): Matplotlib axes to plot on
            parameter (str): The parameter to plot (e.g., 'semi_major_axis')
        """
        title = f"{parameter.replace('_', ' ').title()} Over Time"
        super().__init__(data, ax, title=title)
        
        # Store plot elements
        self.line = None
        self.markers = None
        self.parameter = parameter
    
    def initialize(self):
        """
        Initialize the time series plot.
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Make sure the parameter exists in the data
        if self.parameter not in self.data.columns:
            print(f"Error: Parameter '{self.parameter}' not found in the data")
            return False
        
        # Check for time column
        if 'time' not in self.data.columns:
            print(f"Error: 'time' column not found in the data")
            print(f"Available columns: {self.data.columns.tolist()}")
            return False
            
        # Print some debug info
        print(f"Initializing plot for '{self.parameter}'")
        print(f"Data has {len(self.data)} rows")
        print(f"Time range: {self.data['time'].min()} to {self.data['time'].max()}")
        print(f"{self.parameter} range: {self.data[self.parameter].min()} to {self.data[self.parameter].max()}")
        
        # We'll let plot_manager decide which plots show the x-axis label
        # Only the bottom plot will show it
        
        # Set appropriate y-axis label based on parameter
        if self.parameter == "rotation_angle_deg":
            self.ax.set_ylabel("Angle (degrees)")
        elif self.parameter == "eccentricity":
            self.ax.set_ylabel("Eccentricity")
        elif "axis" in self.parameter:
            self.ax.set_ylabel("Length")
        else:
            self.ax.set_ylabel(f"{self.parameter.replace('_', ' ').title()}")
        
        # Don't set a title to keep plots compact
        self.ax.grid(True, alpha=0.3)  # Lighter grid for less visual noise
        
        # Enable autoscaling for both axes
        self.ax.autoscale(True, 'both', True)
        
        try:
            # Create the line plot
            self.line, = self.ax.plot(
                self.data['time'],
                self.data[self.parameter],
                'b-',  # Blue line
                linewidth=1.5,
                alpha=0.8
            )
            
            # Add markers to show individual data points
            self.markers = self.ax.scatter(
                self.data['time'],
                self.data[self.parameter],
                s=20,  # Marker size
                color='red',
                alpha=0.5
            )
            
            print(f"Plot for '{self.parameter}' created successfully")
            self.is_initialized = True
            return True
        except Exception as e:
            print(f"Error creating plot for '{self.parameter}': {e}")
            return False
    
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
        if self.line is not None:
            self.line.set_xdata(self.data['time'])
            self.line.set_ydata(self.data[self.parameter])
            
        if self.markers is not None:
            self.markers.set_offsets(list(zip(self.data['time'], self.data[self.parameter])))
        
        # Apply axis limits and refresh
        super().update()
        
        return True