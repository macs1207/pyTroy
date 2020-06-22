from utils.transaction import Transaction
import rsa


def generate_address() -> (str, str):
        public, private = rsa.newkeys(512)
        public_key = public.save_pkcs1()
        private_key = private.save_pkcs1()
        return get_address_from_public(public_key), extract_from_private(private_key)


def get_address_from_public(public) -> str:
    address = public.decode('utf-8')
    address = address.replace('\n', '')
    address = address.replace("-----BEGIN RSA PUBLIC KEY-----", '')
    address = address.replace("-----END RSA PUBLIC KEY-----", '')
    return address.strip()


def extract_from_private(private) -> str:
    private_key = private.decode('utf-8')
    private_key = private_key.replace('\n', '')
    private_key = private_key.replace(
        "-----BEGIN RSA PRIVATE KEY-----", '')
    private_key = private_key.replace("-----END RSA PRIVATE KEY-----", '')
    return private_key.strip()


def transaction_to_string(transaction):
    transaction_dict = {
        'sender': str(transaction.sender),
        'receiver': str(transaction.receiver),
        'amounts': transaction.amounts,
        'fee': transaction.fee,
        'message': transaction.message
    }
    return str(transaction_dict)


def get_transactions_string(block):
        transaction_str = ''
        for transaction in block.transactions:
            transaction_str += transaction_to_string(transaction)
        return transaction_str


def initialize_transaction(sender, receiver, amount, fee, message):
    new_transaction = Transaction(sender, receiver, amount, fee, message)
    return new_transaction
