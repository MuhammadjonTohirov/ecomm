# Generated by Django 3.2 on 2022-07-02 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0022_productfield_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcore',
            options={'verbose_name': 'Product Core', 'verbose_name_plural': 'Product List'},
        ),
        migrations.AddField(
            model_name='productfield',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='Visible'),
        ),
        migrations.AlterField(
            model_name='stockproduct',
            name='payment_method',
            field=models.SmallIntegerField(choices=[(0, 'All'), (1, 'Cash'), (2, 'Transfer money')], default=1),
        ),
    ]