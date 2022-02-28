from django.contrib import admin
from .models import Account, Customer, TransactionType, Transaction

# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'balance',
                    'created_date', 'created_by', 'updated_date', 'updated_by', )


class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dob', 'location', 'occupation',
                    'created_date', 'created_by', 'updated_date', 'updated_by', )


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'type', 'credit', 'debit',
                    'created_date', 'created_by', )


admin.site.register(Account, AccountAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(TransactionType, TransactionTypeAdmin)
admin.site.register(Transaction, TransactionAdmin)
