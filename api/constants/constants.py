from enum import Enum

MINIMUM_DEPOSIT_N_TRANSFER = 500.00


class TransactionTypes(Enum):
    DESPOSIT = 'DEPOSIT'
    TRANSFER = 'TRANSFER'
    WIDTHDRAW = 'WIDTHDRAW'


class ValidationErrors(Enum):
    MINIMUM_DEPOSIT = 'Error deposit cannot be less than : '
    MINIMUM_BALANCE_ACCOUNT = ' Error account balance cannot be below: '
    MINIMUM_TRANSFER_AMOUNT = ' Error Transfer amount cannot be less than : '
    UNKNOWN_TRANSACTION = ' Error Transaction type does not exist!'
    CANNOT_TRANSFER_ON_SAME_ACCOUNT = ' Error you can only transfer money between TWO different accouts!'
