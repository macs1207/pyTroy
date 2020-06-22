import time


class Block:
    """
    區塊
    """

    def __init__(self, previous_hash, difficulty, miner, miner_rewards):
        """
        Params:
            previous_hash:  前一個區塊之雜湊值
            hash:           此區塊之雜湊值
            DIFFICULTY:     此區塊之挖掘難度
            nonce:          
            timestamp:      此區塊的產生時間戳
            transactions:   此區塊的交易紀錄
            miner:          此區塊的挖掘者
            miner_rewards:  此區塊的挖掘獎勵
        """
        self.previous_hash = previous_hash
        self.hash = ''
        self.difficulty = difficulty
        self.nonce = 0
        self.timestamp = int(time.time())
        self.transactions = []
        self.miner = miner
        self.miner_rewards = miner_rewards
