import cx_Freeze
import os
import sys

base = None
if sys.platform == 'win32':
    base = "Win32GUI"


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

executables = [cx_Freeze.Executable("AntSimulation.py", base=base, icon="assets/WindowsIcon.ico", trademarks="MrJohnWeez",copyright="MrJohnWeez")]

cx_Freeze.setup(
    name = "Ant Simulation",
    description = 'Ant Pixel Simulator',
    author = 'John Wiesner',
    options = {"build_exe": {"packages": ["pygame"],
                            "include_files":['assets/', os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')],
                            "zip_include_packages" : "*",
                            "zip_exclude_packages" : "",
                            }
                },
                            
    version = '1.0.0',
    executables = executables
    )