import os
import subprocess

path = r'Assingments/Assingments_2/utils/'
filename = ['serverRPS.py', 'ServerTicTacToe.py']

for file in filename:
    subprocess.Popen(['start', 'cmd', '/k', 'python', os.path.join(path, file)], shell=True)