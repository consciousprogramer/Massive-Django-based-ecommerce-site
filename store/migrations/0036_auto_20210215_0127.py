# Generated by Django 3.0.3 on 2021-02-14 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_auto_20210214_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Tags',
            field=models.ManyToManyField(related_name='All_taged_products', to='store.Tag'),
        ),
    ]
