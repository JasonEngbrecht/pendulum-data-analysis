# Pendulum Data Analysis

A tool for visualizing and analyzing pendulum motion data from CSV files. This application provides an easy-to-use interface for exploring pendulum motion patterns through time series plots of key elliptical parameters.

## Features

- **User-friendly interface**: Simple file selection and visualization control
- **Time series visualization**: Plot key elliptical motion parameters over time
  - Semi-major axis
  - Semi-minor axis
  - Rotation angle
  - Eccentricity
- **Optimized plot layout**: All plots are stacked vertically with:
  - No plot titles for a cleaner appearance
  - X-axis tick labels only on the bottom plot
  - X-axis title ("Time (seconds)") only on the bottom plot
  - Synchronized x-axes for easy comparison across parameters
  - Minimal spacing between plots for more efficient use of screen space
- **Synchronized navigation**: Zoom or pan on any plot and all other plots maintain the same x-axis range
- **Customizable views**: Enable/disable specific plots through checkboxes
- **Interactive plots**: Zoom, pan, and save plots with built-in controls
- **Data filtering**: Remove outliers using IQR-based filtering
  - Separate filters for semi-major and semi-minor axes
  - Automatic IQR bounds calculation on file load
  - Manual adjustment of filter bounds
  - Visual feedback showing number of filtered points
  - Easy reset to IQR bounds with dedicated button
- **Future analysis tools**: Curve fitting capabilities coming soon

## Project Structure

```
pendulum-data-analysis/
│
├── main.py                   # Main application entry point
│
├── data/                     # Directory for pendulum data CSV files
│   └── 5-10-25.csv           # Sample data file
│
├── ui/                       # UI components
│   ├── main_window.py        # Main application window
│   ├── file_selector.py      # File selection dialog
│   ├── plot_panel.py         # Panel for displaying plots with synchronized axes
│   └── controls_panel.py     # UI controls for plot selection
│
├── core/                     # Core functionality
│   ├── data_loader.py        # CSV loading and data preparation
│   ├── plot_manager.py       # Manages which plots are displayed
│   ├── filter_manager.py     # Manages data filtering for outlier removal
│   └── analysis.py           # (Future) Analysis and curve fitting
│
├── plots/                    # Plot implementations
│   ├── base_plot.py          # Base class for all plots
│   └── time_series_plot.py   # Time series plots
│
└── utils/                    # Utility functions
    ├── config.py             # Configuration handling
    └── plot_helpers.py       # Helper functions for plot customization
```

## Current Functionality

The application currently allows users to:

1. **Load CSV files** containing pendulum data with the following columns:
   - `date_recorded`, `time_recorded`: Date and time when data was captured
   - `semi_major_axis`, `semi_minor_axis`: Axis measurements of the elliptical motion
   - `rotation_angle_deg`: Rotation angle of the ellipse in degrees
   - `eccentricity`: Eccentricity of the elliptical path

2. **View time series plots** showing how parameters change over time
   - All plots are vertically stacked for easy comparison with minimal spacing
   - X-axes are synchronized across all plots (zooming/panning one plot affects all)
   - X-axis tick labels and "Time (seconds)" label appear only on the bottom plot

3. **Filter outliers** from the data:
   - IQR (Interquartile Range) method automatically calculates suggested bounds
   - Filter controls for semi-major and semi-minor axes
   - Filters can be enabled/disabled independently
   - Manual adjustment of filter min/max values
   - Quick reset to IQR bounds with "IQR" button
   - Real-time display of filtered data statistics
   - All plots reflect the filtered data

4. **Customize the display**:
   - Toggle plots on/off using checkboxes
   - Use built-in matplotlib tools for zooming, panning, and saving plots

## Getting Started

### Prerequisites

- Python 3.7 or higher
- PyQt5
- pandas
- matplotlib
- numpy

### Installation

1. Clone the repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

Run the application using:

```
python main.py
```

## Usage

1. **Open a CSV file**: Use the File menu or Ctrl+O shortcut
2. **Select plot types**: Enable/disable plot types using the checkboxes on the right panel
3. **Filter data** (optional):
   - Check the checkbox next to "Semi-Major Axis" or "Semi-Minor Axis" to enable filtering
   - Adjust the Min/Max values to set filter bounds
   - Click "IQR" to reset to the automatically calculated IQR bounds
   - The status line shows how many points are being displayed/filtered
4. **Interact with plots**: 
   - Use the matplotlib toolbar to zoom, pan, and save plots
   - When zooming or panning any plot, all plots maintain the same x-axis range for easy comparison
   - Use the Reset View button in the View menu to restore the default view

## Data Format

The application expects CSV files with the following columns:
- `date_recorded`: Date in YYYY-MM-DD format
- `time_recorded`: Time in HH:MM:SS format
- `semi_major_axis`: Semi-major axis length of the elliptical motion
- `semi_minor_axis`: Semi-minor axis length of the elliptical motion
- `rotation_angle_deg`: Rotation angle of the ellipse in degrees
- `eccentricity`: Eccentricity of the elliptical path
- Additional columns may be present but are not currently used

## Future Enhancements

- Curve fitting for trend analysis
- Statistical analysis tools
- Multiple data file comparison
- Export of analysis results
