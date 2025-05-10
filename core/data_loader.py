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
            
            print(f"Loaded CSV file: {filepath}")
            print(f"Initial data shape: {self.data.shape}")
            print(f"Initial columns: {self.data.columns.tolist()}")
            
            # Perform basic data validation
            if self._validate_data():
                # Calculate derived quantities if needed
                if self._calculate_derived_values():
                    print("Data processing complete.")
                    return True
                else:
                    print("Failed to calculate derived values.")
                    self.is_loaded = False
                    return False
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
        # Check for required columns for pendulum analysis data
        required_columns = [
            'date_recorded', 'time_recorded', 
            'semi_major_axis', 'semi_minor_axis', 
            'rotation_angle_deg', 'eccentricity'
        ]
        
        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        
        if missing_columns:
            print(f"Missing required columns: {', '.join(missing_columns)}")
            return False
        
        return True
    
    def _calculate_derived_values(self):
        """
        Calculate additional derived values from the raw data.
        Converts date_recorded and time_recorded into a datetime and then into seconds.
        """
        import pandas as pd
        from datetime import datetime
        
        # Create a datetime column by combining date and time
        try:
            # Check if required columns exist
            if 'date_recorded' not in self.data.columns or 'time_recorded' not in self.data.columns:
                print(f"Error: Missing date or time columns. Available columns: {self.data.columns.tolist()}")
                return False
                
            # Combine date and time columns
            self.data['datetime'] = pd.to_datetime(self.data['date_recorded'] + ' ' + self.data['time_recorded'])
            
            # Calculate seconds since start
            start_time = self.data['datetime'].min()
            self.data['time'] = (self.data['datetime'] - start_time).dt.total_seconds()
            
            # Sort by time
            self.data = self.data.sort_values('time')
            
            # Reset index after sorting
            self.data = self.data.reset_index(drop=True)
            
            print(f"Data converted to time series. Time range: {self.data['time'].min()} to {self.data['time'].max()} seconds")
            print(f"Data shape after processing: {self.data.shape}")
            print(f"Columns after processing: {self.data.columns.tolist()}")
            return True
        except Exception as e:
            print(f"Error calculating time series: {e}")
            return False
        
        # Handle any NaN values
        if self.data.isna().any().any():
            self.data = self.data.interpolate(method='linear')
            self.data = self.data.dropna()
    
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
            'semi_major_axis_range': (self.data['semi_major_axis'].min(), self.data['semi_major_axis'].max()) if 'semi_major_axis' in self.data.columns else None,
            'semi_minor_axis_range': (self.data['semi_minor_axis'].min(), self.data['semi_minor_axis'].max()) if 'semi_minor_axis' in self.data.columns else None,
            'rotation_angle_range': (self.data['rotation_angle_deg'].min(), self.data['rotation_angle_deg'].max()) if 'rotation_angle_deg' in self.data.columns else None,
            'eccentricity_range': (self.data['eccentricity'].min(), self.data['eccentricity'].max()) if 'eccentricity' in self.data.columns else None,
        }
