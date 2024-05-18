from django.db import models
# import BaseModel
from crm.models.base_model import BaseModel
# import StockProduct
from wms.models.stock_product import StockInProduct


class ProductUnitConverter(BaseModel):
    product = models.ForeignKey(StockInProduct, on_delete=models.CASCADE,
                                default=None, blank=False, null=True, verbose_name='Product')
    title = models.CharField(
        verbose_name='Unit title', max_length=24, default=None, blank=False, null=True)

    conversion_rate = models.FloatField(max_length=24, default=None, blank=False, null=True,
                                        verbose_name='Conversion Rate', help_text='Conversion rate to base unit')

    def __str__(self):
        return f'{self.title} - {self.conversion_rate}'

    class Meta:
        verbose_name = 'Product unit converter'
        verbose_name_plural = 'Product unit converters'
        db_table = 'wms_productunitconverter'
        ordering = ['title']

    def create_table_sqlite(self):
        return f"""CREATE TABLE IF NOT EXISTS wms_productunitconverter (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            title VARCHAR(24) NOT NULL,
            conversion_rate FLOAT NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            FOREIGN KEY(product_id) REFERENCES wms_stockinproduct(id)
        )"""
