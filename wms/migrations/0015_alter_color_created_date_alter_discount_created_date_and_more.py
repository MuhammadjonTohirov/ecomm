# Generated by Django 4.1.7 on 2023-03-12 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0014_alter_color_created_date_alter_color_updated_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='image',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='productfield',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, verbose_name='Created date'),
        ),
    ]
