# Generated by Django 4.2.1 on 2023-06-01 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_alter_transaction_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='stock',
        ),
    ]
