# Generated by Django 4.1.7 on 2023-09-14 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_trade'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='from_transaction_id',
            field=models.PositiveIntegerField(default=0, help_text='From transaction id', null=True, verbose_name='From transaction id'),
        ),
    ]
