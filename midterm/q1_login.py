import socket
import sys
MAX_BYTES = 1024


def server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Listening at {s.getsockname()}")

        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(MAX_BYTES)
                if not data:
                    break
                else:
                    message = data.decode('UTF-8')
                    print(f"Recv: {message} from {addr}")
                conn.sendall(data)


def client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        message = input("Your Student ID: ")
        data = message.encode('UTF-8')
        s.send(data)
        print("send.")
        data = s.recv(MAX_BYTES)
        print("recv.")
        print("Receiving:", data.decode('UTF-8'))

    print('Received', repr(data))


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
