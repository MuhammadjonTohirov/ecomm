# Generated by Django 4.1.7 on 2023-03-14 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sales', '0003_order_created_by_order_created_date_order_updated_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='cart',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='created_date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Created date'),
        ),
        migrations.AddField(
            model_name='cart',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='updated_date',
            field=models.DateTimeField(auto_created=True, blank=True, null=True, verbose_name='Updated date'),
        ),
    ]
