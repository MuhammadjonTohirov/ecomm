# Generated by Django 4.1.7 on 2023-03-17 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0023_role_created_by_role_updated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='role',
            name='updated_date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Updated date'),
        ),
    ]
