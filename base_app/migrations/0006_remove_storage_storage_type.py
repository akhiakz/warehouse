# Generated by Django 4.0.1 on 2022-05-04 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0005_order_request_storage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='storage_type',
        ),
    ]
