# Generated by Django 4.1.7 on 2023-03-17 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0020_customercard_by_organization_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customercard',
            name='by_organization',
        ),
    ]
