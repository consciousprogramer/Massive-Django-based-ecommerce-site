# Generated by Django 3.0.3 on 2021-02-16 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0043_auto_20210216_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Method',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='Orders', to='store.PaymentMethod'),
        ),
    ]
