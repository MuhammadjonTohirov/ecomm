from crm.models.models import AppConfig


from django.db import models


from typing import List


class ProductCategory(models.Model):
    title = models.CharField(verbose_name='Title', max_length=128, default=None, blank=False, null=True)
    image = models.ImageField(verbose_name='Image', upload_to='images/icons/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)
    description = models.CharField(verbose_name='Description', max_length=512, default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        all_active_configs: List[AppConfig] = AppConfig.objects.all().filter().order_by('-version')
        largest_config: AppConfig = all_active_configs.order_by('-version')[0] if all_active_configs.__len__() != 0 else None
        print(all_active_configs)
        if largest_config is None:
            largest_config = AppConfig.create(version=0, is_active=True, tint_color='#67B8FF', text_color='#757575', background_color='#FFFFFF', created_by=None, updated_by=None)

        largest_config.is_active = True
        largest_config.version += 1
        largest_config.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product category'
        verbose_name_plural = 'Product categories'