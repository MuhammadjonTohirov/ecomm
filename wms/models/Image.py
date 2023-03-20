from crm.models.base_model import BaseModel
from wms.models.folder import Folder

from django.db import models


class Image(BaseModel):
    folder = models.ForeignKey(to=Folder, verbose_name='Folder', blank=True,
                               default=None, related_name='folder', on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name='Image', upload_to='images', default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def save(self):
        for field in self._meta.fields:
            if field.name == 'image':
                field.upload_to = f'images/{self.folder.__str__()}'
        super(Image, self).save()

    def __str__(self) -> str:
        return f'Image - {self.image}'
