# Pendulum Data Analysis

A tool for visualizing and analyzing pendulum motion data from CSV files. This application provides an easy-to-use interface for exploring pendulum motion patterns through time series plots of key elliptical parameters.

## Features

- **User-friendly interface**: Simple file selection and visualization control
- **Time series visualization**: Plot key elliptical motion parameters over time
  - Semi-major axis
  - Semi-minor axis
  - Rotation angle
  - Eccentricity
- **Vertically stacked plots**: All plots are stacked vertically with synchronized x-axes for easy comparison
- **Synchronized navigation**: Zoom or pan on any plot and all other plots will maintain the same x-axis range
- **Customizable views**: Enable/disable specific plots through checkboxes
- **Interactive plots**: Zoom, pan, and save plots with built-in controls
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
│   └── analysis.py           # (Future) Analysis and curve fitting
│
├── plots/                    # Plot implementations
│   ├── base_plot.py          # Base class for all plots
│   └── time_series_plot.py   # Time series plots
│
└── utils/                    # Utility functions
    └── config.py             # Configuration handling
```

## Current Functionality

The application currently allows users to:

1. **Load CSV files** containing pendulum data with the following columns:
   - `date_recorded`, `time_recorded`: Date and time when data was captured
   - `semi_major_axis`, `semi_minor_axis`: Axis measurements of the elliptical motion
   - `rotation_angle_deg`: Rotation angle of the ellipse in degrees
   - `eccentricity`: Eccentricity of the elliptical path

2. **View time series plots** showing how parameters change over time
   - All plots are vertically stacked for easy comparison
   - X-axes are synchronized across all plots (zooming/panning one plot affects all)
   - Time axis (x-axis) labels appear only on the bottom plot to avoid redundancy

3. **Customize the display**:
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
3. **Interact with plots**: 
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

