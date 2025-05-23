# Generated by Django 5.1.6 on 2025-04-20 02:41

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_expense_monthly_expense'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='expenses_list',
        ),
        migrations.AddField(
            model_name='account',
            name='balance',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='income',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='salary',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='saving_goal',
            field=models.FloatField(default=0),
        ),
        migrations.CreateModel(
            name='Liability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.FloatField(default=0)),
                ('date', models.DateField(default=datetime.date(2025, 4, 19))),
                ('long_term', models.BooleanField(default=False)),
                ('interest_rate', models.FloatField(blank=True, default=0, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('monthly_expense', models.FloatField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='liability_list',
            field=models.ManyToManyField(blank=True, to='my_app.liability'),
        ),
        migrations.DeleteModel(
            name='Expense',
        ),
    ]
