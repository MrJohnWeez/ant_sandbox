"""Basic math functions that should be in python"""

def Clamp(n, smallest, largest):
    """Returns a value in range of two values"""
    return max(smallest, min(n, largest))