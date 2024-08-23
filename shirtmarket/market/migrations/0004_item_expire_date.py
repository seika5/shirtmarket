# Generated by Django 4.2.3 on 2023-08-11 03:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_item_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='expire_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
