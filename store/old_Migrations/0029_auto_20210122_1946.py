# Generated by Django 3.0.3 on 2021-01-22 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_auto_20210122_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='productwithvariant',
            name='Name',
            field=models.CharField(default='', max_length=526),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='Product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Attributevalue', to='store.Variant'),
        ),
        migrations.AlterField(
            model_name='productwithvariant',
            name='Name_list',
            field=models.CharField(blank=True, editable=False, max_length=1024),
        ),
    ]
