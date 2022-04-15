from __future__ import unicode_literals
from pyexpat import model
from django.db import models
import string, random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import *



# Create your models here.

# Create your models here.
def account_genarator(length=10, var=string.digits):
    return ''.join(random.choice(var) for _ in range(length))


class AccountDetail(models.Model):
    account_holder = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    account_number = models.CharField(default=account_genarator, max_length=11, unique=True, blank=True, null=True)
    account_balance = models.FloatField(default=0.00)
    account_verified = models.BooleanField(default=False)
    account_ready = models.BooleanField(default=False)
    
    class META:
        verbose_name_plural = 'AccountDetails'

    def __str__(self):
        return f'{self.account_holder} account'

    def __unicode__(self):
        return unicode_literals(self.account_holder)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            AccountDetail.objects.create(account_holder=instance)
    post_save.connect(create_user_profile, sender=User)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)


class Transfer(models.Model):
    sending_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reciver_account = models.CharField(max_length=11)
    reciver_username = models.CharField(max_length=100)
    amount = models.FloatField(default=0.00)
    desc = models.CharField(max_length=200, default='Nil')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.sending_user} transaction detail'

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)

    def save(self, *args, **kwargs):
        super(Transfer, self).save(*args, **kwargs)

class Withdraw(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=99)
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=99)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.sender} withdraw'

class Deposit(models.Model):
    account_holder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)
    deposit = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.account_holder}'