"""
Plot manager for pendulum analysis.
Manages the display and configuration of various plot types.
"""

from utils.config import Config


class PlotManager:
    """
    Manages the creation, configuration, and display of plots for pendulum data analysis.
    """
    
    def __init__(self):
        """Initialize the plot manager."""
        # Initialize plot states (enabled/disabled) based on defaults
        self.plot_states = {}
        for plot_id, plot_info in Config.PLOT_TYPES.items():
            self.plot_states[plot_id] = plot_info['enabled_by_default']
        
        # Initialize axis limits
        self.axis_limits = dict(Config.DEFAULT_AXIS_LIMITS)
        
        # Store references to created plot instances
        self.plots = {}
    
    def get_available_plots(self):
        """
        Get information about all available plot types.
        
        Returns:
            dict: Dictionary of plot types with their information and current enabled state
        """
        result = {}
        for plot_id, plot_info in Config.PLOT_TYPES.items():
            result[plot_id] = {
                **plot_info,
                'enabled': self.plot_states.get(plot_id, False)
            }
        return result
    
    def set_plot_enabled(self, plot_id, enabled):
        """
        Enable or disable a specific plot.
        
        Args:
            plot_id (str): ID of the plot to configure
            enabled (bool): Whether the plot should be enabled
            
        Returns:
            bool: True if successful, False otherwise
        """
        if plot_id not in Config.PLOT_TYPES:
            return False
        
        self.plot_states[plot_id] = enabled
        return True
    
    def is_plot_enabled(self, plot_id):
        """
        Check if a specific plot is enabled.
        
        Args:
            plot_id (str): ID of the plot to check
            
        Returns:
            bool: True if the plot is enabled, False otherwise
        """
        return self.plot_states.get(plot_id, False)
    
    def set_axis_limits(self, x_min=None, x_max=None, y_min=None, y_max=None):
        """
        Set the axis limits for all plots.
        
        Args:
            x_min (float, optional): Minimum X value
            x_max (float, optional): Maximum X value
            y_min (float, optional): Minimum Y value
            y_max (float, optional): Maximum Y value
            
        Returns:
            dict: The current axis limits
        """
        if x_min is not None:
            self.axis_limits['x_min'] = x_min
        if x_max is not None:
            self.axis_limits['x_max'] = x_max
        if y_min is not None:
            self.axis_limits['y_min'] = y_min
        if y_max is not None:
            self.axis_limits['y_max'] = y_max
        
        # Update any existing plots
        for plot in self.plots.values():
            plot.update_axis_limits(self.axis_limits)
        
        return self.axis_limits
    
    def get_axis_limits(self):
        """
        Get the current axis limits.
        
        Returns:
            dict: The current axis limits
        """
        return dict(self.axis_limits)
    
    def create_plots(self, data, figure):
        """
        Create all enabled plots for the given data.
        
        Args:
            data (pandas.DataFrame): The data to plot
            figure (matplotlib.figure.Figure): Figure to draw the plots on
            
        Returns:
            list: List of created plot objects
        """
        # Import the plot classes here to avoid circular imports
        from plots.position_plot import PositionPlot
        from plots.time_series_plot import TimeSeriesPlot
        
        # Clear existing plots
        self.plots = {}
        figure.clear()
        
        # Calculate subplot grid based on number of enabled plots
        enabled_plots = [plot_id for plot_id, enabled in self.plot_states.items() if enabled]
        num_plots = len(enabled_plots)
        
        if num_plots == 0:
            # No plots to display
            return []
        
        # Determine grid size (simple approach: 1 row for 1 plot, 2 rows for 2-4 plots)
        if num_plots == 1:
            rows, cols = 1, 1
        elif num_plots <= 2:
            rows, cols = 1, 2
        else:
            rows = 2
            cols = (num_plots + 1) // 2  # Ceiling division
        
        # Create each enabled plot
        plot_idx = 0
        created_plots = []
        
        for plot_id in enabled_plots:
            if plot_idx >= rows * cols:
                break
                
            # Create a subplot
            ax = figure.add_subplot(rows, cols, plot_idx + 1)
            
            # Create the appropriate plot based on type
            if plot_id == 'position':
                plot = PositionPlot(data, ax)
                self.plots[plot_id] = plot
                created_plots.append(plot)
            elif plot_id in ['x_time_series', 'y_time_series']:
                # Specify which dimension to plot
                dimension = 'x' if plot_id == 'x_time_series' else 'y'
                plot = TimeSeriesPlot(data, ax, dimension=dimension)
                self.plots[plot_id] = plot
                created_plots.append(plot)
            
            # Apply the current axis limits
            plot.update_axis_limits(self.axis_limits)
            
            plot_idx += 1
        
        # Adjust layout
        figure.tight_layout()
        
        return created_plots
    
    def update_plots(self):
        """
        Update all existing plots.
        
        Returns:
            bool: True if successful, False otherwise
        """
        for plot in self.plots.values():
            plot.update()
        return True
