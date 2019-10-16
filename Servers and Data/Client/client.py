import socket

PORT = 1234
MAIN_SERVER_IP = 'localhost'
# this path can be used to store files on client
FILEPATH = '/programming/422062/DS/Mini Project/Distributed File System/Client/'

# TODO
def main():
    '''
    This function contains main logic for client
    '''
    client_socket = socket.socket()

    client_socket.connect((MAIN_SERVER_IP, PORT))

    while True:
        data = client_socket.recv(1024).decode()
        print(data)
        choice = input('Enter choice: ')
        client_socket.send(choice.encode())
        if(choice == '0'):
            print('Taking off the connection ..')
            client_socket.close()
        filedata = client_socket.recv(1024).decode()
        list_of_files = filedata.split('**')
        print('Files stored on the server are server:')
        index_of_files=1
        for file in list_of_files:
            print(str(index_of_files)+'. '+file)
            index_of_files=index_of_files+1
        file_index = int(input('Enter the index of the file you want to download (Enter -1 to skip)\n'))
        if file_index == 0:
            filename='-1';
        else:
            filename=str(list_of_files[file_index-1])
        client_socket.send(filename.encode())
        if filename != '-1':
            file_pointer = open(filename, 'wb')
            filedata = client_socket.recv(1024)
            print('Getting', filename, 'from server...')
            while filedata:
                file_pointer.write(filedata)
                filedata = client_socket.recv(1024)
            print('Got', filename, 'from server.')
            file_pointer.close()
        else:
            print('Going back to menu...')
    client_socket.close()

if __name__ == '__main__':
    main()
