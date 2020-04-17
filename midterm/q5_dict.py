import random
import socket
import sys
import logging

MAX_BYTES = 1024

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    filename="q5.log")



def server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        raw_data = None
        with open("q5_data.txt", "r") as f:
            raw_data = f.readlines()

        
        while True:
            sock, sockname = s.accept()

            logging.info(f"Host: {sockname[0]}, Port: {sockname[0]}")

            data = raw_data.copy()
            
            sock.send(data[0].encode())
            data.pop(0)
            
            next_head = ""
            while len(data) > 500:
                r = random.randint(300, 500)
                tmp_str = next_head + "\n"
                tmp = data[0:r]
                
                for i in range(len(tmp)):
                    if i == (len(tmp) - 1):
                        tmp_split = tmp[i].split()
                        next_head = tmp_split[1]
                        tmp_str += tmp_split[0] + " "
                    else:
                        tmp_str += tmp[i]
                for i in range(r):
                    data.pop(0)
                
                try:
                    sock.send(tmp_str.encode())
                except ConnectionResetError as e:
                    break

            tmp = data
            tmp_str = next_head + "\n"
            for i in range(len(tmp)):
                tmp_str += tmp[i]
                
            try:
                sock.send(tmp_str.encode())
            except ConnectionResetError as e:
                pass
            
            sock.close()
                

def client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        fruit_dict = {}
        message = ""
        while True:
            data = s.recv(MAX_BYTES)
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
