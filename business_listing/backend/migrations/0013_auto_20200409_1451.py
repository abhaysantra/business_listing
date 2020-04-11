# Generated by Django 3.0.5 on 2020-04-09 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_cities_countries_states'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parlour',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='parlour',
            name='created_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='parlour',
            name='status',
            field=models.CharField(default='active', max_length=10),
        ),
    ]