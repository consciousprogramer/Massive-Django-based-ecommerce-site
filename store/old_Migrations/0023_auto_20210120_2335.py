# Generated by Django 3.0.3 on 2021-01-20 18:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_auto_20210120_2042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variant',
            old_name='Image',
            new_name='Mainimage',
        ),
        migrations.AddField(
            model_name='variant',
            name='Created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variant',
            name='Last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='AttributeValue',
            field=models.ManyToManyField(related_name='Variants', to='store.ProductAttributeValue'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='Product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Variants', to='store.Product'),
        ),
        migrations.CreateModel(
            name='VariantImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Created', models.DateTimeField(auto_now_add=True)),
                ('Name', models.CharField(max_length=50)),
                ('Image', models.ImageField(upload_to='product/images/varinat')),
                ('Variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Images', to='store.Variant')),
            ],
        ),
    ]
