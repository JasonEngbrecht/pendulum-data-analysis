"""
Configuration utility for the pendulum data analysis application.
Provides default settings and configuration management.
"""

class Config:
    """
    Configuration class for the pendulum data analysis application.
    Contains default settings and configuration values.
    """
    
    # Application settings
    APP_NAME = "Pendulum Data Analysis"
    APP_VERSION = "0.1.0"
    
    # Default plot settings
    DEFAULT_PLOT_WIDTH = 8
    DEFAULT_PLOT_HEIGHT = 6
    DEFAULT_DPI = 100
    
    # Plot types
    PLOT_TYPES = {
        "position": {
            "name": "Position Plot",
            "description": "X-Y scatter plot of pendulum position",
            "enabled_by_default": True
        },
        "x_time_series": {
            "name": "X Time Series",
            "description": "Plot of X position over time",
            "enabled_by_default": True
        },
        "y_time_series": {
            "name": "Y Time Series",
            "description": "Plot of Y position over time",
            "enabled_by_default": True
        },
        "velocity": {
            "name": "Velocity Plot",
            "description": "Plot of velocity magnitude over time",
            "enabled_by_default": False
        },
        "phase_space": {
            "name": "Phase Space",
            "description": "Position vs. velocity phase space plot",
            "enabled_by_default": False
        }
    }
    
    # Default axis limits
    DEFAULT_AXIS_LIMITS = {
        "x_min": None,  # Auto
        "x_max": None,  # Auto
        "y_min": None,  # Auto
        "y_max": None   # Auto
    }
