import os, subprocess, nicegui
from pathlib import Path

# os.pathsep means it is valid whether it is on Linux/MacOS (:) or Windows (;)

cmd = [
    "python3",
    "-m",
    "PyInstaller",
    "--onefile",
    "--windowed",  # hide console
    # '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui',  # incude nicegui
    f"{Path(__file__).parent}/gui.py",  # entry point
    "--name",
    "DevNotes",
]
subprocess.run(cmd)
