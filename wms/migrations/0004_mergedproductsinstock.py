# Generated by Django 4.1.7 on 2023-09-05 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0003_alter_stockinproduct_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='MergedProductsInStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_quantity', models.PositiveIntegerField(default=0, verbose_name='Total quantity')),
                ('actual_quantity', models.IntegerField(default=0, verbose_name='Actual quantity')),
                ('product', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='wms.productcore', verbose_name='Product')),
                ('transactions', models.ManyToManyField(blank=True, default=None, to='wms.stockinproduct', verbose_name='Transactions')),
            ],
        ),
    ]
