# Generated by Django 3.0.3 on 2021-01-20 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_auto_20210120_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Categorey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='All_products', to='store.SubCategorey'),
        ),
    ]
