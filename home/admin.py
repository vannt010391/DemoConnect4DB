from home.models import AccountType
from django.contrib import admin
from django.contrib.auth.models import User
from home.models import *
# Register your models here.
admin.site.register(AccountType)
admin.site.register(Account)
