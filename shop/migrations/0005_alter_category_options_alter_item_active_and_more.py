# Generated by Django 4.2.1 on 2023-05-28 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_item_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='item',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, default='none/none.jpg', null=True, upload_to='product_images'),
        ),
    ]