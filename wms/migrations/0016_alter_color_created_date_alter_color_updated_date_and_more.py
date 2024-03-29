# Generated by Django 4.1.7 on 2023-03-12 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0015_alter_color_created_date_alter_discount_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='color',
            name='updated_date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Updated date'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='updated_date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Updated date'),
        ),
        migrations.AlterField(
            model_name='image',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='image',
            name='updated_date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Updated date'),
        ),
        migrations.AlterField(
            model_name='productfield',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Created date'),
        ),
        migrations.AlterField(
            model_name='productfield',
            name='updated_date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Updated date'),
        ),
    ]
