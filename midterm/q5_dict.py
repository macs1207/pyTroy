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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    fruit_dict = {}
    message = ""
    while True:
        data = sock.recv(MAX_BYTES)
        if not data:
            break
        message += data.decode('ASCII')
    
    for row in message.split("\n"):
        if row == "":
            continue
        fruit, quantity = row.split(" ")
        if fruit not in fruit_dict.keys():
            fruit_dict[fruit] = 0
        fruit_dict[fruit] += int(quantity)

    for key in sorted(fruit_dict.keys()):
        print(f"{key} {fruit_dict[key]}")
        
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
