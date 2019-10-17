from django.shortcuts import render
import os
import socket

PORT = 1234
MAIN_SERVER_IP = '192.168.43.20'
FILEPATH = './Downloads/'
CONNECTED_TO_SERVER=False
client_socket=None

# Create your views here.
def file_home(request):
    global CONNECTED_TO_SERVER
    global client_socket

    if not CONNECTED_TO_SERVER:
        try:
            client_socket = socket.socket()
            client_socket.connect((MAIN_SERVER_IP, PORT))
            CONNECTED_TO_SERVER=True
        except:
            print('Main Server Down ..')
            CONNECTED_TO_SERVER=False
            
    return render(request,'filesharing/file_home.html')

# Download Views
def download_home(request):
    if request.method == 'POST':
        return render(request,'filesharing/download_home.html')
    else:
        return render(request,'not_found.html')

def download_music(request):
    if request.method == 'POST':
        if request.POST.get("this_contains") == "Music":
            client_socket.send("2".encode())
            file_data = client_socket.recv(1024).decode()
            list_of_files = file_data.split('**')

            return render(request,'filesharing/download_music.html',{"list_of_file":list_of_files})
        elif request.POST.get("object_id"):
            # file_data=request.POST.get("file_data")
            # list_of_files = request.POST.get("list_of_file")
            filename=request.POST.get("object_id") #add up
            client_socket.send(filename.encode())
            if(filename == '0'):  
                return render(request, 'filesharing/download_home.html')
            
            file_pointer = open(FILEPATH + filename, 'wb')
            filedata = client_socket.recv(1024)
            print('Getting', filename, 'from server...')
            while filedata:
                file_pointer.write(filedata)
                filedata = client_socket.recv(1024)
                if filedata[-4:] == b'DONE':
                    filedata = None
                    break
            print('Got', filename, 'from server.')
            file_pointer.close()
            file_data = client_socket.recv(1024).decode()
            list_of_files = file_data.split('**')

            return render(request,'filesharing/download_music.html',{"list_of_file":list_of_files})

    return render(request,'not_found.html')

def download_photos(request):
    if request.method == 'POST':
        if request.POST.get("this_contains") == "Photo":
            client_socket.send("1".encode())
            file_data = client_socket.recv(1024).decode()
            list_of_files = file_data.split('**')

            return render(request,'filesharing/download_photos.html',{"list_of_file":list_of_files})
        elif request.POST.get("object_id"):
            # file_data=request.POST.get("file_data")
            # list_of_files = request.POST.get("list_of_file")
            filename=request.POST.get("object_id") #add up
            client_socket.send(filename.encode())
            if(filename == '0'):
                return render(request, 'filesharing/download_home.html')
            
            file_pointer = open(FILEPATH + filename, 'wb')
            filedata = client_socket.recv(1024)
            print('Getting', filename, 'from server...')
            while filedata:
                file_pointer.write(filedata)
                filedata = client_socket.recv(1024)
                if filedata[-4:] == b'DONE':
                    filedata = None
                    break
            print('Got', filename, 'from server.')
            file_pointer.close()
            file_data = client_socket.recv(1024).decode()
            list_of_files = file_data.split('**')
            
            return render(request,'filesharing/download_photos.html',{"list_of_file":list_of_files})
    return render(request,'not_found.html')


# Upload Views
def upload_home(request):
    return render(request,'filesharing/upload_home.html')
    # return render(request,'not_found.html')

def upload_music(request):
    # return render(request,'filesharing/upload_music.html')
    return render(request,'not_found.html')

def upload_photos(request):
    # return render(request,'filesharing/upload_photos.html')
    return render(request,'not_found.html')
