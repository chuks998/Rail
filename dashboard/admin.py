# import imp
from django.contrib import admin
from .models import AccountDetail, Transfer, Withdraw, Deposit
# Register your models here.

admin.site.register(AccountDetail)
admin.site.register(Transfer)
admin.site.register(Withdraw)
admin.site.register(Deposit)