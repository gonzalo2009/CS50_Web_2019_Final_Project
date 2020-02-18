from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date, datetime

# Create your models here.

class Expense_Type(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="expense_types")

    def __str__(self):
        return f"{self.name}"

class Expense(models.Model):
    expense_type = models.ForeignKey(
        Expense_Type, null=True, on_delete=models.CASCADE, related_name="expenses")
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="expenses")
    amount = models.FloatField(null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.expense_type}"

class Date(models.Model):
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.date}"