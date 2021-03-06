# Generated by Django 3.0.2 on 2020-01-24 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expenses', '0002_expense_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='name',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='user',
        ),
        migrations.CreateModel(
            name='Type_Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='expense',
            name='type_expense',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='expenses.Type_Expense'),
        ),
    ]
