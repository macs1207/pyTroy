class Transaction:
    """
    交易紀錄
    """

    def __init__(self, sender, receiver, amounts, fee, message):
        """        
        Params:
            sender:    此交易之發送方
            receiver:  此交易之收款方
            amounts:   交易金額
            fee:       交易手續費
            message:   備註訊息
        """
        self.sender = sender
        self.receiver = receiver
        self.amounts = amounts
        self.fee = fee
        self.message = message
