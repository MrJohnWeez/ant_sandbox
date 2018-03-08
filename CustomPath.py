import sys
import os

if getattr(sys, 'frozen', False):
    """Returns the os path name"""
    # frozen
    script_dir = os.path.dirname(sys.executable)
else:
    # unfrozen
    script_dir = os.path.dirname(os.path.realpath(__file__))

def Path(localPath):
    """Returns the os path name of the executable"""
    return os.path.join(script_dir, localPath)