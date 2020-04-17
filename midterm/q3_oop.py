
import math
import socket
import sys

MAX_BYTES = 1024


class Rational:

    _numerator = None
    _denominator = None

    def __init__(self, *args):
        if len(args) == 0:
            self._numerator = 0
            self._denominator = 1
        elif len(args) == 1:
            if isinstance(args[0], str):
                tmp_arg = args[0].replace(' ', '').split('/')
                self._numerator = int(tmp_arg[0])
                self._denominator = int(tmp_arg[1])
            elif isinstance(args[0], int):
                self._numerator = args[0]
                self._denominator = 1
            else:
                raise ValueError("Invalid input value.")
        elif len(args) == 2:
            if args[1] == 0:
                raise ValueError("Denominator cannot be zero.")
            self._numerator, self._denominator = args
        else:
            raise ValueError("Invalid input value.")
            
    def reduce(self):
        gcd = math.gcd(self._numerator, self._denominator)
        self._numerator = self._numerator // gcd
        self._denominator = self._denominator // gcd

    def add(self, other):
        new_denominator = self._denominator * other._denominator
        new_numerator = self._numerator * other._denominator + \
            other._numerator * self._denominator
        return Rational(new_numerator, new_denominator)

    def __add__(self, other):
        return self.add(other)

    def __str__(self):
        return f"{self._numerator}/{self._denominator}"


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
        data = s.recv(MAX_BYTES)

        print(data.decode('UTF-8'))
        
        rationals = data.decode('UTF-8').split(" + ")
        
        result = Rational()
        for i in rationals:
            rational = Rational(i)
            result += rational

        result.reduce()
        print(str(result).encode('UTF-8'))
        s.send(str(result).encode('UTF-8'))

        data = s.recv(MAX_BYTES)
        print(data.decode('UTF-8'))

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
