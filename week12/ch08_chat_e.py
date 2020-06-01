import socket
import sys
import threading

MAX_BYTES = 1024
INTERVAL = 1


def recv(sock, e):
    while True:
        data = sock.recv(MAX_BYTES)
        if not data:
            e.set()
            break
        else:
            print(data.decode('UTF-8'))


def send(sock, e):
    while True:
        msg = input()
        sock.send(msg.encode('UTF-8'))

        if msg == 'oo':
            e.set()
            break


def server(host, port):
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listeningSock.bind((host, port))
    listeningSock.listen()
    print("Listening at", listeningSock.getsockname())

    sock, peername = listeningSock.accept()

    e = threading.Event()
    r = threading.Thread(name="server_recv", target=recv,
                         args=(sock, e), daemon=True)
    s = threading.Thread(name="server_send", target=send,
                         args=(sock, e), daemon=True)
    r.start()
    s.start()
    while True:
        if e.wait(INTERVAL):
            break

    sock.close()
    listeningSock.close()


def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connecting from", sock.getsockname(), "to", sock.getpeername())

    e = threading.Event()
    r = threading.Thread(name="client_recv", target=recv,
                         args=(sock, e), daemon=True)
    s = threading.Thread(name="client_send", target=send,
                         args=(sock, e), daemon=True)
    r.start()
    s.start()
    while True:
        if e.wait(INTERVAL):
            break

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


if __name__ == "__main__":
    main()
