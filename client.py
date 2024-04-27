import socket, threading, sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def move_cursor_to_bottom():
    sys.stdout.write("\033[999B")  # Move cursor 999 lines down
    sys.stdout.flush()

def handle_messages(connection: socket.socket):
    '''
        Receive messages sent by the server and display them to user
    '''

    while True:
        try:
            msg = connection.recv(1024)

            # If there is no message, there is a chance that connection has closed
            # so the connection will be closed and an error will be displayed.
            # If not, it will try to decode message in order to show to user.
            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Error handling message from server: {e}')
            connection.close()
            break

def client() -> None:
    '''
        Main process that start client connection to the server 
        and handle it's input messages
    '''

    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 12000

    try:
        # Instantiate socket and start connection with server
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        # Create a thread in order to handle messages sent by server
        threading.Thread(target=handle_messages, args=[socket_instance]).start()
        msg = sys.argv[1]
        socket_instance.send(msg.encode())
        print('Connected to chat!')

        # Read user's input until it quit from chat and close connection
        while True:
            # Move cursor to the bottom
            move_cursor_to_bottom()
            msg = input('> ')
            print ("\033[A                             \033[A")
            print(bcolors.OKGREEN + sys.argv[1] +': '+ bcolors.ENDC + msg)
            # Move cursor to the bottom again
            move_cursor_to_bottom()
            
            if msg == 'quit':
                break

            # Parse message to utf-8
            socket_instance.send(msg.encode())

        # Close connection with the server
        socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        client()
    else:
        print('Enter your username as argument to connect to chat.')