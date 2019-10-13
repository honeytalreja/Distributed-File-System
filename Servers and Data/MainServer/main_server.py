import socket

MAIN_SERVER_PORT = 1234
MAIN_SERVER_IP = '192.168.43.20'
IMAGE_SERVER_PORT = 1235
IMAGE_SERVER_IP = '192.168.43.243'
FILE_SERVER_PORT = 1236
FILE_SERVER_IP = '192.168.43.243'

# DONE
def connect_to_server(ip_addr, port):
    '''
    This function takes input server ip and port number, and returns the socket after establishing a sconnection
    '''
    server_as_client = socket.socket()
    server_as_client.connect((ip_addr, port))
    return server_as_client

# DONE
def send_to_client(socket, filename):
    '''
    Sends the file to client, takes input filename and socket to which client is connected, returns nothing.
    '''
    file_pointer = open(filename, 'rb')
    data = file_pointer.read(1024)
    print('Sending', filename, 'to client...')
    count=10000
    while data:
        socket.send(data)
        data = file_pointer.read(1024)
        count=count-1
    file_pointer.close()
    socket.send(b'DONE')
    print(filename, 'sent to client.')
    return

# DONE
def recv_from_server(socket, filename):
    '''
    Receives file from image or video server, takes input the socket and filename; returns nothing.
    '''
    file_pointer = open(filename, 'wb')
    data = socket.recv(1024)
    print('Receiving', filename, 'from server...')
    count=10000
    while data:
        file_pointer.write(data)
        data = socket.recv(1024)
        # if data == 'DONE':
            # break;
        # count=count-1
    # file_pointer.write(b'done')
        if data[-4:] == b'DONE':
            data = None
            break
        # else: print(str(data[-4:]) + 'apple')

    print(filename, 'received from server.')
    file_pointer.close()
    return

def main():
    '''
    This function contains main logic for main server
    '''
    server_socket = socket.socket()
    server_socket.bind((MAIN_SERVER_IP, MAIN_SERVER_PORT))

    print('Waiting for client to connect...')

    server_socket.listen(5)
    server, addr = server_socket.accept()
    print('Connected to client.')
    menu = '\nBrowse data:\n1.Images\n2.Files'

    while True:
        # server.send(menu.encode())
        choice = int(server.recv(1024).decode())
        print('THIS IS THE CHOICE'+str(choice))
        if choice == 0:
            print('Shutting down the server ..')
            server.close()
        if choice == 1:
            print('Connecting to image server...')
            server_as_client = connect_to_server(IMAGE_SERVER_IP, IMAGE_SERVER_PORT)
            # after making connection loop until client wants to exit
            while True:
                abc='LIST'
                # print('sfdsf')
                server_as_client.send(abc.encode())
                # server_as_client.send('LIST'.encode())
                filedata = server_as_client.recv(1024).decode()
                # FILE_SERVER_IP sends filedata as a string concatenated with '**'
                files = filedata.split('**')
                print('Images present on Image server:')
                print(files)
                for file in files:
                    print(file)
                print('Forwarding information to client.')
                server.send(filedata.encode())

                client_response = server.recv(1024).decode()
                # if client wants to exit
                if client_response == '0':
                    print('Client wants to go to back main menu.')
                    server_as_client.send(b'close')
                    server_as_client.close()
                    break
                    # else client wants the file
                else:
                    filedata = 'GET' + '**' +  client_response
                    server_as_client.send(filedata.encode())
                    # this function receives the file from server
                    recv_from_server(server_as_client, client_response)
                    # now send the file to client
                    send_to_client(server, client_response)
                    print('this is perfect.')

        elif choice == 2:
            server_as_client = connect_to_server(FILE_SERVER_IP, FILE_SERVER_PORT)
            print('Connecting to file server...')
            # server_as_client = connect_to_server(FILE_SERVER_IP, FILE_SERVER_PORT)

            while True:
                abc='LIST'
                # print('sfdsf')
                server_as_client.send(abc.encode())
                # server_as_client.send('LIST'.encode())
                filedata = server_as_client.recv(1024).decode()
                # FILE_SERVER_IP sends filedata as a string concatenated with '**'
                files = filedata.split('**')
                print('Files present on file server:')
                print(files)
                for file in files:
                    print(file)
                print('Forwarding information to client.')
                server.send(filedata.encode())
                client_response = server.recv(1024).decode()
                # if client wants to exit
                if client_response == '0':
                    print('Client wants to go to back main menu.')
                    server_as_client.send(b'close')
                    server_as_client.close()
                    break
                    # else client wants the file
                else:
                    filedata = 'GET' + '**' +  client_response
                    server_as_client.send(filedata.encode())
                    # this function contains receives the file from server code
                    recv_from_server(server_as_client, client_response)
                    # now send the file to client
                    send_to_client(server, client_response)
                    print('this is perfect.')


        else:
            print('Invalid choice by client:', choice)
            break

    server_socket.close()

if __name__ == '__main__':
    main()
