# Generated by Django 3.2 on 2022-05-15 18:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wms', '0004_rename_incomingproduct_stock'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Stock',
            new_name='StockProduct',
        ),
    ]