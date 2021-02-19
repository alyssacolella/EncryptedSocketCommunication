import socket
import sys
import pyDes

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Please include arguments in the following order: script, IP address, port number")
    exit()

# ip address
ip = str(sys.argv[1])

# selected port
port = int(sys.argv[2])

server.bind((ip, port))
server.listen(1)

# conn is socket object, address is client ip address
conn, address = server.accept()

print("Successful connection\n")
fp = open("/Users/alyssacolella/Desktop/3219/SocketCommunication/venv/key.txt", 'r')
key = fp.readline()
print("\nkey:" + key + "\n")

des = pyDes.des("imthekey", pad=None, padmode=pyDes.PAD_PKCS5)

# method to broadcast message from server to client
def respond(chat, connection):
    # if conn != connection:
    try:
        connection.send(chat)
    except:
        print("Failed to send")
        connection.close()


while True:
    try:
        message = conn.recv(1024)
        if message:
            print "Client, encrypted: %r" % message
            print "Client, plaintext: " + des.decrypt(message)
            print "------------------------------------------------------------------------------\n"

            messageBack = sys.stdin.readline()
            sys.stdout.write("Server (you), plaintext: " + messageBack)

            e = des.encrypt(messageBack)
            print "Server (you), encrypted: %r" % e
            print "\n------------------------------------------------------------------------------\n"

            respond(e, conn)

        else:
            conn.close()

    except:
        continue


# end chat, ensure server and client sockets are closed
conn.close()
server.close()








