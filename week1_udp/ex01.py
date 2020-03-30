import socket
import sys
MAX_BYTES = 1024
IP = "192.168.10.80"
PORT = 2020


def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    data, sockname = sock.recvfrom(MAX_BYTES)
    message = data.decode('UTF-8')
    print("Receiving", message, "from", sockname)


def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((host, port))

    message = input("Your Student ID: ")
    data = message.encode('UTF-8')
    sock.send(data)
    print("send.")
    data = sock.recv(MAX_BYTES)
    print("recv.")
    print("Receiving:", data.decode('UTF-8'))
    sock.close()


def main():
    if len(sys.argv) != 4:
        print("Usage: {server|client} host port")
    else:
        host = sys.argv[2]
        port = int(sys.argv[3])
        if sys.argv[1] == "server":
            server(host, port)
        elif sys.argv[1] == "client":
            client(host, port)
        else:
            print("Usage: {server|client} host port")


main()
