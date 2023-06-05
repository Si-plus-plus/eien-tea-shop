# Generated by Django 4.2.1 on 2023-06-04 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_remove_item_image_itemimage_item'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ItemImage',
            new_name='AdditionalItemImage',
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, default='none/none.jpg', null=True, upload_to='item_images'),
        ),
    ]
