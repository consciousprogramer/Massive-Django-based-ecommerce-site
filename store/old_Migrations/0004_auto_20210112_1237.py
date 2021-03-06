# Generated by Django 3.0.3 on 2021-01-12 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_slider_slider_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='slider/images')),
                ('Related_slider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Slide', to='store.Slider')),
            ],
        ),
        migrations.DeleteModel(
            name='Slider_images',
        ),
    ]
