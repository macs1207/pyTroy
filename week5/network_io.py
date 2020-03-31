class NetworkIO:
    def __init__(self, sock):
        pass
    
    def read(self):
        pass
    
    def write(self):
        pass
    

def server(host, port):
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.bind((host, port))
    listeningSock.listen()

    while True:
        sock, sockname = listeningSock.accept()
        handle = NetworkIO(sock)
        while True:
            data = handle.read()
            if not data:
                break
            print('receive', data, 'from', sockname)
        sock.close()

    listeningSock.close()


def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    handle = NetworkIO(sock)
    handle.write(b'NCNU')
    handle.write('Happy Birthday')
    handle.write(5201314)
    handle.write(3.1415926535)

    sock.close()

def main():
    pass

if __name__ == "__main__":
    main()