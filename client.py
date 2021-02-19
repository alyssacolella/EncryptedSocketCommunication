import socket
import sys
import select
import pyDes

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print("Please include arguments in the following order: script, IP address, port number")
    exit()

ip = str(sys.argv[1])
port = int(sys.argv[2])

server.connect((ip, port))

fp = open("/Users/alyssacolella/Desktop/3219/SocketCommunication/venv/key.txt", 'r')
key = fp.readline()
print("\nkey:" + key + "\n")

des = pyDes.des("imthekey", pad=None, padmode=pyDes.PAD_PKCS5)

while True:
    sockets = [sys.stdin, server]
    serverSocket, clientSocket, err = select.select(sockets, [], [])

    for s in serverSocket:
        if s == server:
            message = s.recv(1024)

            print "Server, encrypted: %r" % message
            print "Server, plaintext: " + des.decrypt(message)

            print "------------------------------------------------------------------------------\n"

        else:
            message = sys.stdin.readline()
            e = des.encrypt(message)

            sys.stdout.write("Client (you), plaintext: " + message)
            print "Client (you), encrypted: %r" % e

            server.send(e)

            print "\n------------------------------------------------------------------------------\n"
            sys.stdout.flush()

# close server
server.close()
