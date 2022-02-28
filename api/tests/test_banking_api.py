import copy
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from api.models import Account, TransactionType, Transaction
from api.constants.constants import MINIMUM_DEPOSIT_N_TRANSFER, TransactionTypes

# data

TRANSFER_AMOUNT = 700


def get_credentials():
    credentials = {
        "username": "admin2",
        "password": "A}.9NY/\DM2uw,6#",
        "email": "test@gmail.com"
    }
    return copy.deepcopy(credentials)


def get_customer_object_create():
    customer_object_create = {
        "name": "Elson Musk",
        "dob": "1980-01-31",
        "location": "USA - Hawthorne",
        "occupation": "CEO SpaceX"
    }
    return copy.deepcopy(customer_object_create)


def get_customer_object_update():
    customer_object_update = {
        "name": "Elson Musk",
        "dob": "1980-01-31",
        "location": "USA - Hawthorne",
        "occupation": "CEO SpaceX"
    }
    return copy.deepcopy(customer_object_update)


def get_account_object():
    account_object = {
        "name": "Hiram I",
        "balance": 1200.0,
        "customer_id": -1
    }
    return copy.deepcopy(account_object)


def get_account_object_ii():
    account_object_ii = {
        "name": "Hiram II",
        "balance": 1500.0,
        "customer_id": -1
    }
    return copy.deepcopy(account_object_ii)


def get_transfer_object():
    transfer_object = {
        "from_account": 2,
        "destination_account": 5,
        "amount": 500.00
    }
    return copy.deepcopy(transfer_object)


def get_transaction_type_object():
    transaction_type_object = {'name': TransactionTypes.TRANSFER.value}
    return copy.deepcopy(transaction_type_object)


transaction_type_created = TransactionTypes.TRANSFER.value

# urls
create_user_url = '/auth/users/'
transaction_type_url = '/api/transactiontypes/'
customer_create_url = '/api/customers/'
customer_update_url = '/api/customers/'
account_url = '/api/accounts/'
transfer_url = '/api/transfer/'


def authenticate_client(client):
    create_user_object = get_credentials()
    response = client.post(create_user_url, create_user_object)
    created_user = User.objects.get(
        username=create_user_object["username"])
    user_token = Token.objects.create(user=created_user)
    client.credentials(HTTP_AUTHORIZATION='Token '+user_token.key)
    return client


@pytest.mark.django_db
class TestTransactionTypesOperations:
    def test_anonymous_returns_401(self):
        # AAA
        # Arrange - declaration and initialization
        # Act - request to the server
        # Assert

        # act
        client = APIClient()
        response = client.get(account_url)

        # assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_transaction_type_return_201_created(self):
        client = authenticate_client(APIClient())
        transaction_type_object = get_transaction_type_object()

        response = client.post(transaction_type_url, transaction_type_object)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('name') == transaction_type_created

    def test_create_transaction_type_duplicate_return_400_bad_request(self):
        client = authenticate_client(APIClient())
        transaction_type_object = get_transaction_type_object()

        client.post(transaction_type_url, transaction_type_object)
        count_before = TransactionType.objects.all().count()
        dup_response = client.post(
            transaction_type_url, transaction_type_object)
        assert dup_response.status_code == status.HTTP_400_BAD_REQUEST
        assert count_before == TransactionType.objects.all().count()


@pytest.mark.django_db
class TestCustomerOperations:
    def test_create_customer_return_201_created(self):
        # declaration
        # declaration
        client = authenticate_client(APIClient())
        customer_object_create = get_customer_object_create()

        response = client.post(customer_create_url, customer_object_create)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get(
            'name') == customer_object_create.get('name')
        assert response.data.get(
            'dob') == customer_object_create.get('dob')
        assert response.data.get(
            'location') == customer_object_create.get('location')
        assert response.data.get(
            'occupation') == customer_object_create.get('occupation')

    def test_update_customer_return_201_created(self):
        # declaration
        client = authenticate_client(APIClient())
        customer_object_create = get_customer_object_create()
        customer_object_update = get_customer_object_update()

        create_response = client.post(
            customer_create_url, customer_object_create)
        assert create_response.status_code == status.HTTP_201_CREATED
        # Update
        update_response = client.put(
            f'{ customer_update_url}{create_response.data.get("id")}/', customer_object_update)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data.get(
            'name') == customer_object_update.get('name')
        assert update_response.data.get(
            'dob') == customer_object_update.get('dob')
        assert update_response.data.get(
            'location') == customer_object_update.get('location')
        assert update_response.data.get(
            'occupation') == customer_object_update.get('occupation')


@pytest.mark.django_db
class TestAccountOperations:
    def test_create_account_with_non_existing_customer_return_404(self):
        # declaration
        client = authenticate_client(APIClient())
        account_object = get_account_object()

        response = client.post(f'{account_url}', account_object)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_account_with_no_less_deposit_required_amount_return_403_forbidden(self):
        # declaration
        client = authenticate_client(APIClient())
        account_object = get_account_object()
        customer_object_create = get_customer_object_create()

        create_account_response = client.post(
            customer_create_url, customer_object_create)
        assert create_account_response.status_code == status.HTTP_201_CREATED
        # update customer id
        account_object['customer_id'] = create_account_response.data.get(
            'id')
        # set it to less than required
        account_object['balance'] = MINIMUM_DEPOSIT_N_TRANSFER - 1
        response = client.post(f'{account_url}', account_object)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_account_for_available_customer_with_required_deposit_amount_With_no_deposit_transaction_type_return_404(self):

        # declaration
        client = authenticate_client(APIClient())
        account_object = get_account_object()
        customer_object_create = get_customer_object_create()
        transaction_type_object = get_transaction_type_object()

        create_account_response = client.post(
            customer_create_url, customer_object_create)
        assert create_account_response.status_code == status.HTTP_201_CREATED
        # update customer id
        account_object['customer_id'] = create_account_response.data.get(
            'id')
        # set it to less than required
        account_object['balance'] = MINIMUM_DEPOSIT_N_TRANSFER
        # create transaction type for deposit first
        transaction_type_object['name'] = TransactionTypes.WIDTHDRAW.value
        transaction_type_response = client.post(
            transaction_type_url, transaction_type_object)
        assert transaction_type_response.status_code == status.HTTP_201_CREATED
        assert transaction_type_response.data.get(
            'name') == TransactionTypes.WIDTHDRAW.value
        transaction_recs = Transaction.objects.all().count()
        response = client.post(f'{account_url}', account_object)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert transaction_recs == Transaction.objects.all().count()

    def test_create_account_for_available_customer_with_required_deposit_amount_return_201_created(self):
        # declaration
        client = authenticate_client(APIClient())
        account_object = get_account_object()
        customer_object_create = get_customer_object_create()
        transaction_type_object = get_transaction_type_object()

        create_account_response = client.post(
            customer_create_url, customer_object_create)
        assert create_account_response.status_code == status.HTTP_201_CREATED
        # update customer id
        account_object['customer_id'] = create_account_response.data.get(
            'id')
        # set it to less than required
        account_object['balance'] = MINIMUM_DEPOSIT_N_TRANSFER
        # create transaction type for deposit first
        transaction_type_object['name'] = TransactionTypes.DESPOSIT.value
        transaction_type_response = client.post(
            transaction_type_url, transaction_type_object)
        assert transaction_type_response.status_code == status.HTTP_201_CREATED
        assert transaction_type_response.data.get(
            'name') == TransactionTypes.DESPOSIT.value
        transaction_recs = Transaction.objects.all().count()
        response = client.post(f'{account_url}', account_object)
        assert response.status_code == status.HTTP_201_CREATED
        assert transaction_recs+1 == Transaction.objects.all().count()


@pytest.mark.django_db
class TestTransferOperations:
    def test_transfer_less_than_required_amount_403_forbidden(self):
        # declaration
        client = authenticate_client(APIClient())
        account_object = get_account_object()
        transfer_object = get_transfer_object()
        customer_object_create = get_customer_object_create()
        transaction_type_object = get_transaction_type_object()
        account_object_ii = get_account_object_ii()

        create_customer_response = client.post(
            customer_create_url, customer_object_create)
        assert create_customer_response.status_code == status.HTTP_201_CREATED

        # transaction types
        transaction_type_object['name'] = TransactionTypes.DESPOSIT.value
        transaction_type_response = client.post(
            transaction_type_url, transaction_type_object)
        assert transaction_type_response.status_code == status.HTTP_201_CREATED

        # update customer id
        customer_id = create_customer_response.data.get('id')
        account_object['customer_id'] = customer_id

        from_account = client.post(f'{account_url}', account_object)
        assert from_account.status_code == status.HTTP_201_CREATED
        from_account_id = from_account.data.get('id')
        # # destination
        account_object_ii['customer_id'] = customer_id
        destination_account = client.post(f'{account_url}', account_object)
        assert destination_account.status_code == status.HTTP_201_CREATED
        destination_account_id = destination_account.data.get('id')

        # # transfer transaction type
        transaction_type_object['name'] = TransactionTypes.TRANSFER.value
        transaction_type_transanfer_response = client.post(
            transaction_type_url, transaction_type_object)
        assert transaction_type_transanfer_response.status_code == status.HTTP_201_CREATED

        # # transfer amount
        transfer_object['from_account'] = from_account_id
        transfer_object['destination_account'] = destination_account_id
        transfer_object['amount'] = MINIMUM_DEPOSIT_N_TRANSFER - 1

        response = client.post(transfer_url, transfer_object)
        print(response)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_transfer_super_pass_minimum_account_balance_403_forbidden(self):
        # declaration
        client = authenticate_client(APIClient())
        account_object = get_account_object()
        transfer_object = get_transfer_object()
        customer_object_create = get_customer_object_create()
        transaction_type_object = get_transaction_type_object()
        account_object_ii = get_account_object_ii()

        create_customer_response = client.post(
            customer_create_url, customer_object_create)
        assert create_customer_response.status_code == status.HTTP_201_CREATED

        # transaction types
        transaction_type_object['name'] = TransactionTypes.DESPOSIT.value
        transaction_type_response = client.post(
            transaction_type_url, transaction_type_object)
        assert transaction_type_response.status_code == status.HTTP_201_CREATED

        # update customer id
        customer_id = create_customer_response.data.get('id')
        account_object['customer_id'] = customer_id

        from_account = client.post(f'{account_url}', account_object)
        assert from_account.status_code == status.HTTP_201_CREATED
        from_account_id = from_account.data.get('id')
        # # destination
        account_object_ii['customer_id'] = customer_id
        destination_account = client.post(f'{account_url}', account_object)
        assert destination_account.status_code == status.HTTP_201_CREATED
        destination_account_id = destination_account.data.get('id')

        # # transfer transaction type
        transaction_type_object['name'] = TransactionTypes.TRANSFER.value
        transaction_type_transanfer_response = client.post(
            transaction_type_url, transaction_type_object)
        assert transaction_type_transanfer_response.status_code == status.HTTP_201_CREATED

        # # transfer amount
        transfer_object['from_account'] = from_account_id
        transfer_object['destination_account'] = destination_account_id
        # balance should be below minimu account balance
        # from balance =1200, transfer 800, balance = 400 which is less than minimum balance
        transfer_object['amount'] = 800
        response = client.post(transfer_url, transfer_object)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_transfer_from_unknown_account_404(self):
        # declaration
        client = authenticate_client(APIClient())
        account_object = get_account_object()
        transfer_object = get_transfer_object()
        customer_object_create = get_customer_object_create()
        transaction_type_object = get_transaction_type_object()
        account_object_ii = get_account_object_ii()

        create_customer_response = client.post(
            customer_create_url, customer_object_create)
        assert create_customer_response.status_code == status.HTTP_201_CREATED

        # transaction types
        transaction_type_object['name'] = TransactionTypes.DESPOSIT.value
        transaction_type_response = client.post(
            transaction_type_url, transaction_type_object)
        assert transaction_type_response.status_code == status.HTTP_201_CREATED

        # update customer id
        customer_id = create_customer_response.data.get('id')
        account_object['customer_id'] = customer_id

        # # destination
        account_object_ii['customer_id'] = customer_id
        destination_account = client.post(f'{account_url}', account_object)
        assert destination_account.status_code == status.HTTP_201_CREATED
        destination_account_id = destination_account.data.get('id')

        # # transfer transaction type
        transaction_type_object['name'] = TransactionTypes.TRANSFER.value
        transaction_type_transanfer_response = client.post(
            transaction_type_url, transaction_type_object)
        assert transaction_type_transanfer_response.status_code == status.HTTP_201_CREATED

        # # transfer amount
        transfer_object['from_account'] = -1
        transfer_object['destination_account'] = destination_account_id
        # balance should be below minimu account balance
        # from balance =1200, transfer 700, balance = 5400 which is equal to minimum balance
        transfer_object['amount'] = 700
        response = client.post(transfer_url, transfer_object)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_transfer_to_unknown_account_return_404(self):
        # declaration
        client = authenticate_client(APIClient())
        account_object = get_account_object()
        transfer_object = get_transfer_object()
        customer_object_create = get_customer_object_create()
        transaction_type_object = get_transaction_type_object()

        create_customer_response = client.post(
            customer_create_url, customer_object_create)
        assert create_customer_response.status_code == status.HTTP_201_CREATED

        # transaction types
        transaction_type_object['name'] = TransactionTypes.DESPOSIT.value
        transaction_type_response = client.post(
            transaction_type_url, transaction_type_object)
        assert transaction_type_response.status_code == status.HTTP_201_CREATED

        # update customer id
        customer_id = create_customer_response.data.get('id')
        account_object['customer_id'] = customer_id

        from_account = client.post(f'{account_url}', account_object)
        assert from_account.status_code == status.HTTP_201_CREATED
        from_account_id = from_account.data.get('id')
        # # transfer transaction type
        transaction_type_object['name'] = TransactionTypes.TRANSFER.value
        transaction_type_transanfer_response = client.post(
            transaction_type_url, transaction_type_object)
        assert transaction_type_transanfer_response.status_code == status.HTTP_201_CREATED

        # # transfer amount
        transfer_object['from_account'] = from_account_id
        transfer_object['destination_account'] = -1
        transfer_object['amount'] = 700
        response = client.post(transfer_url, transfer_object)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_transfer_correct_amount_correct_miniumum_balance_to_correct_from_to_accounts_return_200_ok(self):
        # declaration
        client = authenticate_client(APIClient())
        account_object = get_account_object()
        transfer_object = get_transfer_object()
        customer_object_create = get_customer_object_create()
        transaction_type_object = get_transaction_type_object()
        account_object_ii = get_account_object_ii()

        create_customer_response = client.post(
            customer_create_url, customer_object_create)
        assert create_customer_response.status_code == status.HTTP_201_CREATED

        # transaction types
        transaction_type_object['name'] = TransactionTypes.DESPOSIT.value
        transaction_type_response = client.post(
            transaction_type_url, transaction_type_object)
        assert transaction_type_response.status_code == status.HTTP_201_CREATED

        # update customer id
        customer_id = create_customer_response.data.get('id')
        account_object['customer_id'] = customer_id

        from_account = client.post(f'{account_url}', account_object)
        assert from_account.status_code == status.HTTP_201_CREATED
        from_account_id = from_account.data.get('id')
        from_account_initial_balance = from_account.data.get('balance')
        # destination
        account_object_ii['customer_id'] = customer_id
        destination_account = client.post(f'{account_url}', account_object)
        assert destination_account.status_code == status.HTTP_201_CREATED
        destination_account_id = destination_account.data.get('id')
        destination_account_intial_balance = destination_account.data.get(
            'balance')

        # # transfer transaction type
        transaction_type_object['name'] = TransactionTypes.TRANSFER.value
        transaction_type_transanfer_response = client.post(
            transaction_type_url, transaction_type_object)
        assert transaction_type_transanfer_response.status_code == status.HTTP_201_CREATED

        # # transfer amount
        transaction_records = Transaction.objects.all().count()
        transfer_object['from_account'] = from_account_id
        transfer_object['destination_account'] = destination_account_id
        transfer_object['amount'] = TRANSFER_AMOUNT
        response = client.post(transfer_url, transfer_object)
        assert response.status_code == status.HTTP_200_OK

        # check trasactions
        assert transaction_records+2 == Transaction.objects.all().count()

        # check account balances
        update_from_account = Account.objects.get(pk=from_account_id)
        update_destination_account = Account.objects.get(
            pk=destination_account_id)

        # assert
        print('from_account_initial_balance', from_account_initial_balance)
        print('from final balance ', update_from_account.balance)

        print('destination_account_intial_balance',
              destination_account_intial_balance)
        print('destination final balance ', update_destination_account.balance)

        assert update_from_account.balance == from_account_initial_balance - TRANSFER_AMOUNT
        assert update_destination_account.balance == destination_account_intial_balance + TRANSFER_AMOUNT
