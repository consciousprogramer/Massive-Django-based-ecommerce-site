# Generated by Django 3.0.3 on 2021-01-22 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_auto_20210122_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='productwithvariant',
            name='Is_active',
            field=models.BooleanField(default=True, verbose_name='Product Status'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='Is_active',
            field=models.BooleanField(default=True, verbose_name='Product Status'),
        ),
    ]
