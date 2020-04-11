# Generated by Django 3.0.5 on 2020-04-09 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_auto_20200409_0317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parlour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=255, null=True)),
                ('landmark', models.CharField(max_length=255, null=True)),
                ('country', models.IntegerField(null=True)),
                ('state', models.IntegerField(null=True)),
                ('city', models.IntegerField(null=True)),
                ('pincode', models.CharField(max_length=255, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='parlour/profile/')),
                ('status', models.CharField(default='active', max_length=8)),
                ('created_date', models.DateField(null=True)),
                ('created_by', models.IntegerField(null=True)),
                ('modified_date', models.DateField(null=True)),
                ('modified_by', models.IntegerField(null=True)),
                ('address', models.TextField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
