
import math
import socket
import sys

MAX_BYTES = 1024


class Rational:

    _numerator = None
    _denominator = None

    def __init__(self, numerator, denominator):
        self._numerator = numerator
        self._denominator = denominator

    def reduce(self):
        gcd = math.gcd(self._numerator, self._denominator)
        self._numerator = self._numerator // gcd
        self._denominator = self._denominator // gcd

    def add(self, other):
        return self + other

    def __add__(self, other):
        new_denominator = self._denominator * other._denominator
        new_numerator = self._numerator * other._denominator + \
            other._numerator * self._denominator
        return Rational(new_numerator, new_denominator)

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
        
        result = Rational(int(rationals[0].split("/")[0]), int(rationals[0].split("/")[1]))
        for i in rationals[1:]:
            rational = Rational(int(i.split("/")[0]), int(i.split("/")[1]))
            result = result.add(rational)

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
