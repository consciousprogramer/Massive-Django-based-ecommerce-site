# Generated by Django 3.0.3 on 2021-01-28 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0046_auto_20210128_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Thumbnail_path',
            field=models.CharField(blank=True, editable=False, max_length=164),
        ),
    ]
