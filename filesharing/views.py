from django.shortcuts import render
import os
import socket

PORT = 1234
MAIN_SERVER_IP = '192.168.43.20'
FILEPATH = './'
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
        client_socket.send("2".encode())
        file_data = client_socket.recv(1024).decode()
        list_of_files = filedata.split('**')
    return render(request,'filesharing/download_music.html')
    return render(request,'not_found.html')

def download_photos(request):
    # return render(request,'filesharing/download_photos.html')
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
