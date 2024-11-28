import os
import subprocess
# Start the server for the RPS and TicTacToe games
path = r'Assingments/Assingments_2/utils/'
filename = ['serverRPS.py', 'ServerTicTacToe.py']

for file in filename:
    subprocess.Popen(['start', 'cmd', '/k', 'python', os.path.join(path, file)], shell=True)