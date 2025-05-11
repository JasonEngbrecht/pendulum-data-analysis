"""
Helpers for matplotlib plots.
"""

import matplotlib.pyplot as plt


def fix_bottom_axis_ticks(axes_list):
    """
    Make sure the bottom axis shows tick labels and the rest don't.
    
    Args:
        axes_list: List of matplotlib axes
    """
    if not axes_list:
        return
    
    # Hide tick labels on all but the bottom plot
    for i, ax in enumerate(axes_list):
        if i < len(axes_list) - 1:  # Not the bottom axis
            plt.setp(ax.get_xticklabels(), visible=False)
            ax.set_xlabel('')
        else:  # Bottom axis
            # Let matplotlib handle the labels normally
            ax.set_xlabel('Time (seconds)')
