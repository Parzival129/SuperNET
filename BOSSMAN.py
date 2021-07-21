import socket, threading
print ("test")
server_private_key = "8d6fsdfh39ur893uruf86we7f58734y uihuhUYGIUDHS*&AD9d8 3yuh78y(*iu(d*&D"

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
                if server_private_key in msg.decode():
                    print("This is a server message")
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

        print('Connected to BOTNET!')

        # Read user's input until it quit from chat and close connection
        count = 0
        while True:
            if count == 4:
                socket_instance = socket.socket()
                socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
                count = 0
            msg = input("Command >> ")

            sent_message = server_private_key + msg
            msg = sent_message

            if msg == 'quit':
                break
            # Parse message to utf-8
            socket_instance.send(msg.encode())
            count += 1

        # Close connection with the server
        socket_instance.close()
        print ("closed connection with server")
        quit()
        exit()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()


if __name__ == "__main__":
    client()
