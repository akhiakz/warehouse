# Generated by Django 4.0.1 on 2022-05-06 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0008_contact_us_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_us',
            name='replay_status',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]