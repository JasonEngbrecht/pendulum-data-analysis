"""
Data loader for pendulum analysis.
Handles loading and preprocessing CSV data.
"""

import pandas as pd
import numpy as np
import os


class DataLoader:
    """
    Handles loading and processing pendulum data from CSV files.
    """
    
    def __init__(self):
        """Initialize the data loader."""
        self.data = None
        self.filename = None
        self.is_loaded = False
    
    def load_csv(self, filepath):
        """
        Load data from a CSV file.
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            return False
        
        try:
            # Load the data
            self.data = pd.read_csv(filepath)
            self.filename = os.path.basename(filepath)
            self.is_loaded = True
            
            # Perform basic data validation
            if self._validate_data():
                # Calculate derived quantities if needed
                self._calculate_derived_values()
                return True
            else:
                self.is_loaded = False
                return False
                
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            self.is_loaded = False
            return False
    
    def _validate_data(self):
        """
        Validate that the loaded data has the required columns.
        
        Returns:
            bool: True if data is valid, False otherwise
        """
        # Check if the CSV has the expected columns for pendulum data
        # This will depend on the exact format of your CSV files
        # For now, we'll check for basic x, y coordinates
        
        required_columns = []
        
        # Check for columns related to position
        position_columns = ['x', 'y']
        time_column = 'time'
        
        # Look for variations of column names
        for col in self.data.columns:
            col_lower = col.lower()
            if any(pos in col_lower for pos in ['x_pos', 'x position', 'x-position', 'x']):
                position_columns[0] = col
            elif any(pos in col_lower for pos in ['y_pos', 'y position', 'y-position', 'y']):
                position_columns[1] = col
            elif any(t in col_lower for t in ['time', 'timestamp', 't']):
                time_column = col
        
        required_columns = position_columns + [time_column]
        
        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        
        if missing_columns:
            print(f"Missing required columns: {', '.join(missing_columns)}")
            return False
        
        return True
    
    def _calculate_derived_values(self):
        """
        Calculate additional derived values from the raw data.
        For example: velocity, acceleration, etc.
        """
        # This method will be expanded as needed
        # For now, we'll just ensure the data is properly formatted
        
        # Make sure we have a time column
        if 'time' not in self.data.columns and 't' in self.data.columns:
            self.data['time'] = self.data['t']
        
        # If there are NaN values, interpolate or drop them
        if self.data.isna().any().any():
            self.data = self.data.interpolate(method='linear')
            self.data = self.data.dropna()
        
        # Sort by time if it exists
        if 'time' in self.data.columns:
            self.data = self.data.sort_values('time')
        
        # TODO: Add calculations for velocity, acceleration, etc.
    
    def get_data(self):
        """
        Get the loaded data.
        
        Returns:
            pandas.DataFrame: The loaded data, or None if no data is loaded
        """
        return self.data if self.is_loaded else None
    
    def get_column_names(self):
        """
        Get the column names from the loaded data.
        
        Returns:
            list: List of column names, or empty list if no data is loaded
        """
        return list(self.data.columns) if self.is_loaded else []
    
    def get_data_summary(self):
        """
        Get a summary of the loaded data.
        
        Returns:
            dict: Summary of the loaded data, or empty dict if no data is loaded
        """
        if not self.is_loaded:
            return {}
        
        return {
            'filename': self.filename,
            'rows': len(self.data),
            'columns': self.get_column_names(),
            'time_range': (self.data['time'].min(), self.data['time'].max()) if 'time' in self.data.columns else None,
            'x_range': (self.data['x'].min(), self.data['x'].max()) if 'x' in self.data.columns else None,
            'y_range': (self.data['y'].min(), self.data['y'].max()) if 'y' in self.data.columns else None,
        }
