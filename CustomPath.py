import sys
import os


if getattr(sys, 'frozen', False):
    # frozen
    script_dir = os.path.dirname(sys.executable)
else:
    # unfrozen
    script_dir = os.path.dirname(os.path.realpath(__file__))

def Path(localPath):
    return os.path.join(script_dir, localPath)