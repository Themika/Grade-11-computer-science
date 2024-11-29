import os
import subprocess
# Start the server for the RPS and TicTacToe games
path = r'utils/'  # Path to the folder containing the scripts
filename = ['serverRPS.py', 'ServerTicTacToe.py']  # List of files to execute

for file in filename:
    subprocess.Popen(['start', 'cmd', '/k', 'python', os.path.join(path, file)], shell=True)
