# Generated by Django 3.0.3 on 2021-01-23 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_auto_20210123_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategorey',
            name='Show_on_mainpage',
            field=models.BooleanField(default=False),
        ),
    ]
