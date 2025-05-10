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
        "semi_major_axis": {
            "name": "Semi-Major Axis",
            "description": "Plot of semi-major axis over time",
            "enabled_by_default": True
        },
        "semi_minor_axis": {
            "name": "Semi-Minor Axis",
            "description": "Plot of semi-minor axis over time",
            "enabled_by_default": True
        },
        "rotation_angle_deg": {
            "name": "Rotation Angle",
            "description": "Plot of rotation angle over time",
            "enabled_by_default": True
        },
        "eccentricity": {
            "name": "Eccentricity",
            "description": "Plot of eccentricity over time",
            "enabled_by_default": True
        }
    }
    
    # Default axis limits
    DEFAULT_AXIS_LIMITS = {
        "x_min": None,  # Auto
        "x_max": None,  # Auto
        "y_min": None,  # Auto
        "y_max": None   # Auto
    }
