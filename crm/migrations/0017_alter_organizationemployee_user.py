# Generated by Django 4.1.7 on 2023-03-13 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0016_organizationemployee_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationemployee',
            name='user',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=255, unique=True, verbose_name='Username'),
        ),
    ]
