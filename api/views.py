from http.client import BAD_REQUEST, FORBIDDEN, OK
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .constants.constants import TransactionTypes, ValidationErrors, MINIMUM_DEPOSIT_N_TRANSFER

from .models import Account, Customer, Transaction, TransactionType
from .serializers import AccountDisplaySerializer, TransactionSerializer, TransferSerializer, TransactionTypeSerializer, CustomerSerializer, AccountSaveSerializer
import logging

from api import serializers
# Create your views here.

# logging
logger = logging.getLogger(__name__)
# logger.debug


def MinimumAccountBalance(value):
    return value < MINIMUM_DEPOSIT_N_TRANSFER


# get transaction type
def get_transaction_type(transaction_name):
    transaction_type = TransactionTypeSerializer(
        get_object_or_404(TransactionType, name=transaction_name))
    if transaction_type.data == None:
        return Response(ValidationErrors.UNKNOWN_TRANSACTION.value, status=FORBIDDEN)
    return transaction_type


def save_transaction_details(account, credit, debit, transaction_type_id):
    transaction = Transaction(
        account_id=account, credit=credit, debit=debit, type_id=transaction_type_id, created_by="Admin")
    transaction.save()
    return transaction


def update_account_details(account_id, balance):
    account = get_object_or_404(Account, pk=account_id)
    account.balance = balance
    account.updated_date = datetime.utcnow()
    account.save()
    return account


# Transaction types operations
class TransactionTypesViewSet(ModelViewSet):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
    http_method_names = ['head', 'get', 'post']

    def get_serializer_context(self):
        return {'request': self.request}


# customers - operations
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    http_method_names = ['head', 'get', 'post', 'put']

    def get_serializer_context(self):
        return {'request': self.request}


# get customer accounts
@api_view(['GET'])
def customer_accounts(request, id):
    customer_obj = get_object_or_404(Customer, pk=id)
    accounts = Account.objects.filter(customer=customer_obj)
    serializer = AccountDisplaySerializer(accounts, many=True)
    return Response(serializer.data)


# Accounts - operations
class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSaveSerializer
    http_method_names = ['head', 'get', 'post']

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        logger.info(f"creating account logger")
        serializer = AccountSaveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Customer exist
        valid_data = serializer.validated_data
        deposit = valid_data.get('balance')
        customer_account = valid_data.get('customer_id')
        logger.info(f"check if customer exist")
        get_object_or_404(
            Customer, pk=customer_account)
        # insert into transaction operations
        if(MinimumAccountBalance(deposit)):
            logger.error(ValidationErrors.MINIMUM_DEPOSIT.value)
            return Response(f'{str(ValidationErrors.MINIMUM_DEPOSIT.value)} { MINIMUM_DEPOSIT_N_TRANSFER}', status=FORBIDDEN)
        transaction_type = get_transaction_type(
            TransactionTypes.DESPOSIT.value)
        # create account
        serializer.save()
        created_account = serializer.data.get('id')
        logger.info(f"account created: {created_account}")
        logger.info(f"insert into transaction table the deposit: {deposit}")
        # save to transaction table
        save_transaction_details(
            created_account, deposit, 0.00, transaction_type.data.get('id'))
        logger.info(f"account creation, and depositing cash finished")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@ api_view(['GET'])
def account_history_all(request, id):
    logger.info(f"get account history, account: {id}")
    get_object_or_404(Account, pk=id)
    transactions = Transaction.objects.filter(account_id=id)
    serializer = TransactionSerializer(transactions, many=True)
    logger.info(f"return account transaction history")
    return Response(serializer.data)


# cash transfer operations
class TransferViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransferSerializer
    http_method_names = ['head', 'post']

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        logger.info(f"{__name__}- initiate cash transfer")
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validate_data = serializer.validated_data
        amount = validate_data.get('amount')
        from_account = validate_data.get('from_account')
        destination_account = validate_data.get('destination_account')
        logger.info(
            f" transfer {amount} from {from_account} to {destination_account}")
        if(from_account == destination_account):
            logger.erro(ValidationErrors.CANNOT_TRANSFER_ON_SAME_ACCOUNT.value)
            return Response(f'{ValidationErrors.CANNOT_TRANSFER_ON_SAME_ACCOUNT.value}', status=FORBIDDEN)

        if(MinimumAccountBalance(amount)):
            logger.error(ValidationErrors.MINIMUM_BALANCE_ACCOUNT.value)
            return Response(F'{ValidationErrors.MINIMUM_BALANCE_ACCOUNT.value} {MINIMUM_DEPOSIT_N_TRANSFER}', status=FORBIDDEN)
        # check if accounts exist
        logger.info(f"checking if from account: {from_account} exist")
        from_acc_details = AccountDisplaySerializer(
            get_object_or_404(Account, pk=from_account))
        logger.info(
            f"checking if destination account: {destination_account} exist")
        destination_acc_details = AccountDisplaySerializer(get_object_or_404(
            Account, pk=destination_account))
        # Enforce minimum account balance
        logger.info(f"checking if from account: {from_account}  balance ")
        from_balance = from_acc_details.data.get('balance') - amount
        destination_balance = destination_acc_details.data.get(
            'balance') + amount
        if(MinimumAccountBalance(from_balance)):
            logger.error(
                f'{ValidationErrors.MINIMUM_BALANCE_ACCOUNT} {MINIMUM_DEPOSIT_N_TRANSFER}')
            return Response(f'{ValidationErrors.MINIMUM_BALANCE_ACCOUNT.value} { MINIMUM_DEPOSIT_N_TRANSFER}', status=FORBIDDEN)
        # save transcation details
        # get transaction type
        logger.info(
            f"saving transaction both credit and debit on two different accounts")
        transaction_type = get_transaction_type(
            TransactionTypes.TRANSFER.value)
        save_transaction_details(from_account, 0.00, amount,
                                 transaction_type.data.get('id'))
        save_transaction_details(destination_account, amount,
                                 0.00, transaction_type.data.get('id'))
        # update balance for account
        logger.info(f"update the balance in customer actual account")
        result = update_account_details(from_account, from_balance)
        update_account_details(destination_account, destination_balance)
        logger.info(f"transfer complete")
        return Response(AccountDisplaySerializer(result).data, status=OK)
