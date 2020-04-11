# Generated by Django 3.0.5 on 2020-04-11 14:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_parlourservice_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parlourservice',
            name='uuid',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=100, null=True, unique=True),
        ),
    ]
