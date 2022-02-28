from xmlrpc.client import DateTime
from datetime import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.


class TransactionType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(TransactionType, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=255)
    dob = models.DateField()
    location = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255)
    updated_date = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True,  blank=True)

    def save(self, *args, **kwargs):
        self.created_by = "Admin"
        return super(Customer, self).save(*args, **kwargs)


class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # deposit less than a million
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255)
    updated_date = models.DateTimeField(null=True,  blank=True)
    updated_by = models.CharField(max_length=255,  null=True, blank=True)


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    debit = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255)
