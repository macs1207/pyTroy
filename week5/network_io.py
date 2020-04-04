import socket
import struct
import sys


class NetworkIO:
    
    sock = None
    
    def __init__(self, sock):
        self.sock = sock
    
    def read(self):
        data = self._nbyte_to_data(self.sock)
        if not data:
            return None
        return f"{type(data).__name__} {repr(data)}"
        
        
    def write(self, n):
        self.sock.send(self._data_to_nbyte(n))
    
    def _data_to_nbyte(self, n):
        if isinstance(n, int):
            if n < (1 << 8):
                tag = b'B'
            elif n < (1 << 16):
                tag = b'H'
            elif n < (1 << 32):
                tag = b"L"
            else:
                tag = b'Q'
            result = tag + struct.pack('!' + tag.decode(), n)
            return result
        elif isinstance(n, bytes):
            result = b's' + self._data_to_nbyte(len(n)) + n
            return result
        elif isinstance(n, str):
            n = n.encode('UTF-8')
            result = b'c' + self._data_to_nbyte(len(n)) + n
            return result
        elif isinstance(n, float):
            result = b'd' + struct.pack('!d', n)
            return result
        raise TypeError('Invalid type: ' + str(type(n)))


    def _nbyte_to_data(self, sock):
        size_info = {'B': 1, 'H': 2, 'L': 4, 'Q': 8}

        btag = sock.recv(1)
        if not btag:
            return None
        else:
            tag = btag.decode('UTF-8')

        if tag in size_info:
            size = size_info[tag]
            bnum = sock.recv(size)
            result = struct.unpack('!' + tag, bnum)[0]
        elif tag in "sc":
            size = self._nbyte_to_data(sock)
            if size >= 65536:
                raise ValueError('length too long: ' + str(size))
            bstr = sock.recv(size)
            if tag == 's':
                result = bstr
            else:
                result = bstr.decode('UTF-8')
        elif tag == "d":
            bnum = sock.recv(8)
            result = struct.unpack("!d", bnum)[0]
        else:
            raise TypeError('Invalid type: ' + tag)
        return result
    

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
