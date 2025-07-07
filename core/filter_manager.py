"""
Filter manager for pendulum analysis.
Handles data filtering based on IQR method for outlier removal.
"""

import numpy as np
import pandas as pd


class FilterManager:
    """
    Manages data filtering for pendulum analysis.
    Applies IQR-based filtering on semi-major and semi-minor axes.
    """
    
    def __init__(self):
        """Initialize the filter manager."""
        self.original_data = None
        self.filter_settings = {
            'semi_major_axis': {
                'enabled': False,
                'min': None,
                'max': None,
                'iqr_min': None,
                'iqr_max': None
            },
            'semi_minor_axis': {
                'enabled': False,
                'min': None,
                'max': None,
                'iqr_min': None,
                'iqr_max': None
            }
        }
    
    def set_data(self, data):
        """
        Set the data and calculate IQR bounds.
        
        Args:
            data (pandas.DataFrame): The original data
        """
        self.original_data = data.copy()
        self._calculate_iqr_bounds()
    
    def _calculate_iqr_bounds(self):
        """Calculate IQR bounds for semi-major and semi-minor axes."""
        if self.original_data is None:
            return
        
        for axis in ['semi_major_axis', 'semi_minor_axis']:
            if axis in self.original_data.columns:
                # Calculate quartiles
                q1 = self.original_data[axis].quantile(0.25)
                q3 = self.original_data[axis].quantile(0.75)
                iqr = q3 - q1
                
                # Calculate bounds using 1.5 * IQR rule
                iqr_min = q1 - 1.5 * iqr
                iqr_max = q3 + 1.5 * iqr
                
                # Store IQR bounds
                self.filter_settings[axis]['iqr_min'] = iqr_min
                self.filter_settings[axis]['iqr_max'] = iqr_max
                
                # Set initial filter bounds to IQR bounds
                self.filter_settings[axis]['min'] = iqr_min
                self.filter_settings[axis]['max'] = iqr_max
                
                print(f"{axis} IQR bounds: [{iqr_min:.2f}, {iqr_max:.2f}]")
    
    def set_filter_enabled(self, axis, enabled):
        """
        Enable or disable filtering for a specific axis.
        
        Args:
            axis (str): 'semi_major_axis' or 'semi_minor_axis'
            enabled (bool): Whether to enable the filter
        """
        if axis in self.filter_settings:
            self.filter_settings[axis]['enabled'] = enabled
            print(f"Filter for {axis}: {'enabled' if enabled else 'disabled'}")
    
    def set_filter_bounds(self, axis, min_val=None, max_val=None):
        """
        Set the filter bounds for a specific axis.
        
        Args:
            axis (str): 'semi_major_axis' or 'semi_minor_axis'
            min_val (float, optional): Minimum value
            max_val (float, optional): Maximum value
        """
        if axis in self.filter_settings:
            if min_val is not None:
                self.filter_settings[axis]['min'] = min_val
            if max_val is not None:
                self.filter_settings[axis]['max'] = max_val
            print(f"Updated {axis} bounds: min={self.filter_settings[axis]['min']:.2f}, max={self.filter_settings[axis]['max']:.2f}")
    
    def get_filter_settings(self):
        """
        Get the current filter settings.
        
        Returns:
            dict: Current filter settings
        """
        return self.filter_settings.copy()
    
    def get_filtered_data(self):
        """
        Get the filtered data based on current settings.
        
        Returns:
            pandas.DataFrame: Filtered data
        """
        if self.original_data is None:
            return None
        
        # Start with all data
        filtered_data = self.original_data.copy()
        mask = pd.Series([True] * len(filtered_data))
        
        # Apply filters for each axis
        for axis in ['semi_major_axis', 'semi_minor_axis']:
            if (self.filter_settings[axis]['enabled'] and 
                axis in filtered_data.columns):
                
                min_val = self.filter_settings[axis]['min']
                max_val = self.filter_settings[axis]['max']
                
                if min_val is not None or max_val is not None:
                    # Create mask for this axis
                    if min_val is not None and max_val is not None:
                        # Check for invalid range
                        if min_val > max_val:
                            print(f"WARNING: {axis} has min ({min_val:.2f}) > max ({max_val:.2f}) - this will filter out all data!")
                        axis_mask = (filtered_data[axis] >= min_val) & (filtered_data[axis] <= max_val)
                    elif min_val is not None:
                        axis_mask = filtered_data[axis] >= min_val
                    else:  # max_val is not None
                        axis_mask = filtered_data[axis] <= max_val
                    # Combine with overall mask using AND (point must pass both filters)
                    mask = mask & axis_mask
                    
                    # Debug: print how many points pass this filter
                    points_passing = axis_mask.sum()
                    print(f"  {axis}: {points_passing} points pass filter")
        
        # Apply the combined mask
        filtered_data = filtered_data[mask].copy()
        
        # Print filtering statistics
        original_count = len(self.original_data)
        filtered_count = len(filtered_data)
        removed_count = original_count - filtered_count
        
        if removed_count > 0:
            print(f"Filtering removed {removed_count} of {original_count} points ({removed_count/original_count*100:.1f}%)")
        
        return filtered_data
    
    def get_filter_stats(self):
        """
        Get statistics about the current filtering.
        
        Returns:
            dict: Statistics including original count, filtered count, and removed count
        """
        if self.original_data is None:
            return {
                'original_count': 0,
                'filtered_count': 0,
                'removed_count': 0,
                'removed_percentage': 0.0
            }
        
        filtered_data = self.get_filtered_data()
        original_count = len(self.original_data)
        filtered_count = len(filtered_data)
        removed_count = original_count - filtered_count
        
        return {
            'original_count': original_count,
            'filtered_count': filtered_count,
            'removed_count': removed_count,
            'removed_percentage': (removed_count / original_count * 100) if original_count > 0 else 0.0
        }
    
    def reset_filters(self):
        """Reset all filters to default state (disabled with IQR bounds)."""
        for axis in ['semi_major_axis', 'semi_minor_axis']:
            self.filter_settings[axis]['enabled'] = False
            # Reset bounds to IQR bounds if available
            if self.filter_settings[axis]['iqr_min'] is not None:
                self.filter_settings[axis]['min'] = self.filter_settings[axis]['iqr_min']
                self.filter_settings[axis]['max'] = self.filter_settings[axis]['iqr_max']
