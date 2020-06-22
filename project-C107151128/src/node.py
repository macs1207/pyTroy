from utils.block import Block
from utils.transaction import Transaction
from utils.functions import generate_address, transaction_to_string, get_transactions_string
import hashlib
import pickle
import socket
import threading
import time
import logging
import rsa


HOST = "127.0.0.1"
PORT = 10028
MAX_LENGTH = 4096

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%y-%m-%d %H:%M')


class BlockChain:
    """
    區塊鏈

    Attributes:
        DIFFICULTY:              區塊挖掘的難度
        ADJUST_DIFFICULTY_FREQ:  調整區塊挖掘難度的頻率
        BLOCK_TIME:              出塊時間之理想值，當實際出塊時間小於此值則調升難度，反之亦然
        MINER_REWARDS:           挖掘者獎勵金額
        BLOCK_LIMITATION:        每個區塊容納的交易數量上限
    """
    ADJUST_DIFFICULTY_FREQ = 5
    DIFFICULTY = 5
    BLOCK_TIME = 30
    MINER_REWARDS = 10
    BLOCK_LIMITATION = 32

    def __init__(self, host, port):
        self.chain = []  # 該區塊鏈的所有區塊
        self.pending_transactions = []  # 儲存 pending status (未處理) 的交易

        self.host = host
        self.port = port
        self.start_socket_server()

    def create_genesis_block(self):
        """
        建立創世塊(第一個區塊)
        """
        print("Create genesis block...")
        new_block = Block('2020-06-22 Hello block!', self.DIFFICULTY,
                          'Macs', self.MINER_REWARDS)
        new_block.hash = self.get_hash(new_block, 0)
        self.chain.append(new_block)

    def get_hash(self, block, nonce) -> str:
        """
        根據
            1. 前一個區塊的 hash 值
            2. 區塊產生的時間戳
            3. 區塊的交易紀錄
            4. 隨機值
        產生此區塊的 hash 值
        """
        s = hashlib.sha1()
        s.update(
            (
                block.previous_hash
                + str(block.timestamp)
                + get_transactions_string(block)
                + str(nonce)
            ).encode("utf-8")
        )
        h = s.hexdigest()
        return h

    def add_transaction_to_block(self, block):
        """
        將交易紀錄儲存到區塊中，優先處理手續費高的交易
        """
        self.pending_transactions.sort(key=lambda x: x.fee, reverse=True)
        if len(self.pending_transactions) > self.BLOCK_LIMITATION:
            transcation_accepted = self.pending_transactions[:self.BLOCK_LIMITATION]
            self.pending_transactions = self.pending_transactions[self.BLOCK_LIMITATION:]
        else:
            transcation_accepted = self.pending_transactions
            self.pending_transactions = []
        logging.info(
            f"Accept {len(transcation_accepted)} transactions to block.")
        block.transactions = transcation_accepted

    def mine_block(self, miner):
        """
        挖掘新的區塊，並處理等待中的交易，記錄到區塊中
        """
        start = time.process_time()

        last_block = self.chain[-1]
        new_block = Block(last_block.hash, self.DIFFICULTY,
                          miner, self.MINER_REWARDS)

        self.add_transaction_to_block(new_block)
        new_block.previous_hash = last_block.hash
        new_block.DIFFICULTY = self.DIFFICULTY
        new_block.hash = self.get_hash(new_block, new_block.nonce)

        while new_block.hash[0: self.DIFFICULTY] != '0' * self.DIFFICULTY:
            new_block.nonce += 1
            new_block.hash = self.get_hash(new_block, new_block.nonce)

        time_consumed = round(time.process_time() - start, 5)
        logging.info(
            f"Hash found: {new_block.hash} @ DIFFICULTY {self.DIFFICULTY}, time: {time_consumed}")
        self.chain.append(new_block)

    def adjust_difficulty(self):
        """
        依據出塊時間之平均值調整挖掘難度
        """
        if len(self.chain) % self.ADJUST_DIFFICULTY_FREQ != 1:
            return self.DIFFICULTY
        elif len(self.chain) <= self.ADJUST_DIFFICULTY_FREQ:
            return self.DIFFICULTY
        else:
            start = self.chain[-1 * self.ADJUST_DIFFICULTY_FREQ-1].timestamp
            finish = self.chain[-1].timestamp
            average_time_consumed = round(
                (finish - start) / self.ADJUST_DIFFICULTY_FREQ, 2)
            if average_time_consumed > self.BLOCK_TIME:
                logging.info(
                    f"Average block time: {average_time_consumed}s. Lower the DIFFICULTY")
                self.DIFFICULTY -= 1
            else:
                logging.info(
                    f"Average block time: {average_time_consumed}s. High up the DIFFICULTY")
                self.DIFFICULTY += 1

    def get_balance(self, account) -> int:
        """
        計算該帳戶餘額，餘額包含
            1. 區塊挖掘獎勵
            2. 區塊之手續費收入
            3. 他人匯款收入
        """
        balance = 0
        for block in self.chain:
            miner = False
            if block.miner == account:
                miner = True
                balance += block.miner_rewards
            for transaction in block.transactions:
                if miner:
                    balance += transaction.fee
                if transaction.sender == account:
                    balance -= transaction.amounts
                    balance -= transaction.fee
                elif transaction.receiver == account:
                    balance += transaction.amounts
        return balance

    def verify_blockchain(self) -> bool:
        """
        依據區塊 Hash 驗證是否包含偽造交易紀錄
        """
        previous_hash = ''
        for idx, block in enumerate(self.chain):
            if self.get_hash(block, block.nonce) != block.hash:
                logging.error("Hash not matched!")
                return False
            elif previous_hash != block.previous_hash and idx:
                logging.error("Hash not matched to previous_hash")
                return False
            previous_hash = block.hash
        logging.info("Hash correct!")
        return True

    def add_transaction(self, transaction, signature):
        """
        新增交易紀錄
        """
        public_key = '-----BEGIN RSA PUBLIC KEY-----\n'
        public_key += transaction.sender
        public_key += '\n-----END RSA PUBLIC KEY-----\n'
        public_key_pkcs = rsa.PublicKey.load_pkcs1(public_key.encode('utf-8'))
        transaction_str = transaction_to_string(transaction)
        if transaction.fee + transaction.amounts > self.get_balance(transaction.sender):
            return False, "Balance not enough!"
        try:
            # 驗證發送者
            rsa.verify(transaction_str.encode('utf-8'),
                       signature, public_key_pkcs)
            self.pending_transactions.append(transaction)
            return True, "Authorized successfully!"
        except Exception:
            return False, "RSA Verified wrong!"

    def start(self):
        """
        啟動區塊鏈，行為包含
            1. 建立第一個錢包地址
            2. 建立創世塊(第一個區塊)
            3. 挖掘新區塊並調整挖掘難度
        """
        address, private = generate_address()
        logging.info(f"Miner address: {address}")
        logging.info(f"Miner private: {private}")
        
        self.create_genesis_block()
        while(True):
            self.mine_block(address)
            self.adjust_difficulty()

    def start_socket_server(self):
        """
        啟動區塊鏈之 socket server
        """
        t = threading.Thread(target=self.wait_for_conn)
        t.start()

    def wait_for_conn(self):
        """
        等待連線，有新連線則以新執行緒執行 handler
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                conn, client = s.accept()

                client_handler = threading.Thread(
                    target=self.receive_socket_message,
                    args=(conn, client)
                )
                client_handler.start()

    def receive_socket_message(self, conn, client):
        """
        處理 client 的請求，包含
            1. 取得餘額
            2. 匯款
        """
        with conn:
            logging.info(f'Connected by: {client}')
            while True:
                message = conn.recv(MAX_LENGTH)
                # print(f"[*] Received: {message}")
                try:
                    parsed_message = pickle.loads(message)
                except Exception:
                    logging.error(f"{message} cannot be parsed")
                if message:
                    if parsed_message["request"] == "get_balance":
                        logging.info("Start to get the balance for client.")
                        address = parsed_message["address"]
                        balance = self.get_balance(address)
                        response = {
                            "address": address,
                            "balance": balance
                        }
                        logging.info("Get the balance for client done.")
                    elif parsed_message["request"] == "transaction":
                        logging.info("Start to transaction for client.")
                        new_transaction = parsed_message["data"]
                        result, result_message = self.add_transaction(
                            new_transaction,
                            parsed_message["signature"]
                        )
                        response = {
                            "result": result,
                            "result_message": result_message
                        }
                        logging.info("Transact for client done.")
                    else:
                        response = {
                            "message": "Unknown command."
                        }
                    response_bytes = str(response).encode('utf8')
                    conn.sendall(response_bytes)


if __name__ == '__main__':
    block = BlockChain(HOST, PORT)
    block.start()
