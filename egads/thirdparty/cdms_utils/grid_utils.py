"""
grid_utils.py
=============


Some utilities for working with CDMS grids.

"""

# Import python modules

# Import third-party software
import axis_utils

def compareGrids(grid1, grid2):
    """
    Takes 2 cdms grid objects returning 1 if they are essentially
    the same and 0 if not."""
    if axis_utils.areAxesIdentical(grid1.getLatitude(),
                                   grid2.getLatitude(), check_id=False)==False:
        return False
    if axis_utils.areAxesIdentical(grid1.getLongitude(),
                                   grid2.getLongitude(), check_id=False)==False:
        return False
    return True
