# Generated by Django 3.0.5 on 2020-04-06 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20200406_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile/'),
        ),
    ]
