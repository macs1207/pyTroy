# ch08_listen
# The "backlog" parameter in socket.socket.listen()

import socket, sys
MAX_BYTES = 1024

def server(host, port):
    BACKLOG = 1
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.bind( (host, port) )
    listeningSock.listen(BACKLOG)

    print("Listening at", listeningSock.getsockname())
    while True:
        sock, sockname = listeningSock.accept()
        data = sock.recv(MAX_BYTES)
        message = data.decode('UTF-8')
        print("Receiving", message, "from", sockname)
        sock.close()

    listeningSock.close()

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (host, port) )

    message = input("? ")
    data = message.encode('UTF-8')
    sock.send(data)

    sock.close()

def main():
    msg = "Usage: %s {server|client} host port" % sys.argv[0]
    if len(sys.argv) != 4:
        print(msg)
    else:
        host = sys.argv[2]
        port = int(sys.argv[3])
        if sys.argv[1] == "server":
            server(host, port)
        elif sys.argv[1] == "client":
            client(host, port)
        else:
            print(msg)

main()
