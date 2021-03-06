# Generated by Django 3.0.3 on 2021-02-02 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20210131_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='Customer',
            new_name='User',
        ),
        migrations.AlterField(
            model_name='customer',
            name='ProfilePic',
            field=models.ImageField(blank=True, default='./store/images/avatar/avt.png', upload_to='profiles/profilepics'),
        ),
    ]
