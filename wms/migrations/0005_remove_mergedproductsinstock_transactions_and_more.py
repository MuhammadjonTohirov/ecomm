# Generated by Django 4.1.7 on 2023-09-05 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0004_mergedproductsinstock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mergedproductsinstock',
            name='transactions',
        ),
        migrations.AddField(
            model_name='mergedproductsinstock',
            name='transactions',
            field=models.TextField(default='[]', help_text='JSON array of transactions', verbose_name='Transactions'),
        ),
    ]
