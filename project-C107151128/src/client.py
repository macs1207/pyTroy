from utils.transaction import Transaction
from utils.functions import generate_address, transaction_to_string, initialize_transaction
import pickle
import socket
import threading
import rsa


HOST = "127.0.0.1"
PORT = 10028
MAX_LENGTH = 4096


def handle_receive(sock):
    while True:
        response = sock.recv(MAX_LENGTH)
        if response:
            print(f"[*] Message from node: {response}")

def sign_transaction(transaction, private):
    private_key = f"-----BEGIN RSA PRIVATE KEY-----\n{private}\n-----END RSA PRIVATE KEY-----\n"
    private_key_pkcs = rsa.PrivateKey.load_pkcs1(private_key.encode('utf-8'))
    transaction_str = transaction_to_string(transaction)
    signature = rsa.sign(transaction_str.encode(
        'utf-8'), private_key_pkcs, 'SHA-1')
    return signature

def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    receive_handler = threading.Thread(target=handle_receive, args=(sock, ))
    receive_handler.start()

    command_dict = {
        "1": "generate_address",
        "2": "get_balance",
        "3": "transaction"
    }

    while True:
        print("Command list:")
        for command in command_dict:
            print(f"{command}: {command_dict[command]}")
        print()
        command = input("Command: ")
        if command not in command_dict.keys():
            print("Unknown command.")
            continue
        message = {
            "request": command_dict[command]
        }
        if command_dict[command] == "generate_address":
            address, private_key = generate_address()
            print(f"Address: {address}")
            print(f"Private key: {private_key}")

        elif command_dict[command] == "get_balance":
            address = input("Address: ")
            message['address'] = address
            sock.send(pickle.dumps(message))

        elif command_dict[command] == "transaction":
            address = input("Address: ")
            private_key = input("Private_key: ")
            receiver = input("Receiver: ")
            amount = input("Amount: ")
            fee = input("Fee: ")
            comment = input("Comment: ")
            new_transaction = initialize_transaction(
                address, receiver, int(amount), int(fee), comment
            )
            signature = sign_transaction(new_transaction, private_key)
            message["data"] = new_transaction
            message["signature"] = signature

            sock.send(pickle.dumps(message))


if __name__ == "__main__":
    client()
