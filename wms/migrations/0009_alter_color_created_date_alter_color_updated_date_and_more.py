# Generated by Django 4.1.7 on 2023-03-07 18:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0008_alter_image_created_by_alter_image_updated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime.now, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='color',
            name='updated_date',
            field=models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime.now, verbose_name='Updated date'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime.now, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='updated_date',
            field=models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime.now, verbose_name='Updated date'),
        ),
        migrations.AlterField(
            model_name='image',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime.now, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='image',
            name='updated_date',
            field=models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime.now, verbose_name='Updated date'),
        ),
        migrations.AlterField(
            model_name='productfield',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime.now, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='productfield',
            name='updated_date',
            field=models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime.now, verbose_name='Updated date'),
        ),
    ]