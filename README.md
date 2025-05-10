# Pendulum Data Analysis

A tool for visualizing and analyzing pendulum motion data from CSV files. This application provides an easy-to-use interface for exploring pendulum motion patterns and performing various analyses.

## Features

- **User-friendly interface**: Simple file selection and visualization control
- **Multiple plot types**: Position plots, time series, and more
- **Customizable views**: Adjust axis limits for detailed examination
- **Interactive plots**: Zoom, pan, and save plots with built-in controls
- **Future analysis tools**: Curve fitting capabilities coming soon

## Project Structure

```
pendulum-data-analysis/
│
├── main.py                   # Main application entry point
│
├── data/                     # Directory to store example CSV files
│
├── ui/                       # UI components
│   ├── main_window.py        # Main application window
│   ├── file_selector.py      # File selection dialog
│   ├── plot_panel.py         # Panel for displaying plots
│   └── controls_panel.py     # UI controls for plots (on/off toggles, axis limits)
│
├── core/                     # Core functionality
│   ├── data_loader.py        # CSV loading and data preparation
│   ├── plot_manager.py       # Manages which plots are displayed
│   └── analysis.py           # (Future) Analysis and curve fitting
│
├── plots/                    # Plot implementations
│   ├── base_plot.py          # Base class for all plots
│   ├── position_plot.py      # X-Y position scatter plot
│   └── time_series_plot.py   # Time series plots
│
└── utils/                    # Utility functions
    └── config.py             # Configuration handling
```

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
2. **Select plot types**: Enable/disable plot types using the checkboxes
3. **Adjust axis limits**: Set custom axis limits or use "Auto" for automatic scaling
4. **Interact with plots**: Use the toolbar to zoom, pan, and save plots

## Data Format

The application expects CSV files with the following columns:
- Time column (named "time", "t", or similar)
- Position columns (named "x", "y", "x_pos", "y_pos", or similar)

## Future Enhancements

- Curve fitting for sinusoidal motion analysis
- Frequency analysis tools
- Energy calculations
- Multiple data file comparison
- 3D visualization for complex pendulum motion
