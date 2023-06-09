# Generated by Django 4.2.1 on 2023-06-02 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.CharField(max_length=100)),
                ('shipping_address', models.CharField(max_length=150)),
                ('shipping_notes', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(default='Indonesia', max_length=50)),
                ('postal_code', models.CharField(max_length=10)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
