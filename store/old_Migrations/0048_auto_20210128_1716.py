# Generated by Django 3.0.3 on 2021-01-28 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0047_auto_20210128_1658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Thumbnail_path',
            new_name='Thumb_path',
        ),
        migrations.RenameField(
            model_name='product_images',
            old_name='Images',
            new_name='Main_image',
        ),
        migrations.RenameField(
            model_name='variantimages',
            old_name='Image',
            new_name='Main_image',
        ),
        migrations.RemoveField(
            model_name='productwithvariant',
            name='Thumbnail',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='Thumbnail',
        ),
        migrations.RemoveField(
            model_name='variantimages',
            name='thumb',
        ),
        migrations.AddField(
            model_name='fileshare',
            name='Text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='product_images',
            name='Thumb_path',
            field=models.CharField(blank=True, editable=False, max_length=164),
        ),
        migrations.AddField(
            model_name='productwithvariant',
            name='Thumb_path',
            field=models.CharField(blank=True, editable=False, max_length=164),
        ),
        migrations.AddField(
            model_name='variant',
            name='Thumb_path',
            field=models.CharField(blank=True, editable=False, max_length=164),
        ),
        migrations.AddField(
            model_name='variantimages',
            name='Thumb_path',
            field=models.CharField(blank=True, editable=False, max_length=164),
        ),
    ]
