# Generated by Django 5.1.5 on 2025-02-09 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_payment_printer_terminal_delete_printerstatus_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='price_document',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=5, verbose_name='Цена'),
        ),
    ]
