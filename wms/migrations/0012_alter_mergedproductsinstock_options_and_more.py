# Generated by Django 4.1.7 on 2023-09-06 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0011_mergedproductsinstock_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mergedproductsinstock',
            options={'verbose_name': 'Merged product in stock', 'verbose_name_plural': 'Merged products in stock'},
        ),
        migrations.AlterField(
            model_name='mergedproductsinstock',
            name='product',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='wms.productcore', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='mergedproductsinstock',
            name='stock_point',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wms.stockpoint3'),
        ),
        migrations.AlterUniqueTogether(
            name='mergedproductsinstock',
            unique_together={('product', 'stock_point')},
        ),
        migrations.AlterModelTable(
            name='mergedproductsinstock',
            table='merged_products_in_stock',
        ),
    ]