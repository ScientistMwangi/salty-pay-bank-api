from pyexpat import model
from rest_framework import serializers
from django.db import models
from .models import Customer, Account, Transaction, TransactionType
from django.utils import timezone
from datetime import datetime


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ['id', 'name']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'dob', 'location', 'occupation']


class AccountDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_number', 'name', 'balance', 'customer']
    account_number = serializers.PrimaryKeyRelatedField(
        read_only=True, source='id')
    name = serializers.CharField(max_length=255)
    balance = serializers.DecimalField(
        max_digits=6, decimal_places=2, default=0.00)
    customer = CustomerSerializer()


class AccountSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'customer_id']
    id = serializers.IntegerField(read_only=True)
    # initial_deposit = serializers.DecimalField(
    #    max_digits=6, decimal_places=2, default=0.00, source='balance')
    customer_id = serializers.IntegerField()


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['account', 'type', 'cash_in', 'cash_out', 'transaction_date']
    type = TransactionTypeSerializer()
    account = AccountDisplaySerializer()
    cash_in = serializers.DecimalField(
        max_digits=6, decimal_places=2, default=0.00, source='credit')
    cash_out = serializers.DecimalField(
        max_digits=6, decimal_places=2, default=0.00, source='debit')
    transaction_date = serializers.DateTimeField(
        default=timezone.now, source='created_date')


class TransferSerializer(serializers.Serializer):
    from_account = serializers.IntegerField()
    destination_account = serializers.IntegerField()
    amount = serializers.DecimalField(
        max_digits=6, decimal_places=2, default=0.00)
