# Generated by Django 3.0.3 on 2021-02-16 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0044_auto_20210216_0719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='Products',
        ),
        migrations.RemoveField(
            model_name='order',
            name='Variants',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='Order',
            field=models.ForeignKey(default=13, on_delete=django.db.models.deletion.CASCADE, related_name='Orderprod', to='store.Order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordervariant',
            name='Order',
            field=models.ForeignKey(default=13, on_delete=django.db.models.deletion.CASCADE, related_name='Ordervar', to='store.Order'),
            preserve_default=False,
        ),
    ]
