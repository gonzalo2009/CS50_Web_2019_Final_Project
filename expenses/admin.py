from django.contrib import admin
from .models import Expense_Type, Expense, Date

# Register your models here.
admin.site.register(Expense_Type)
admin.site.register(Expense)
admin.site.register(Date)
