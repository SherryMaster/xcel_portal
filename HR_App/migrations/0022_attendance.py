# Generated by Django 5.0 on 2023-12-22 14:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0021_profile_is_logged_in_alter_profile_profile_month'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('month', models.CharField(max_length=2)),
                ('day', models.CharField(max_length=2)),
                ('minute', models.CharField(max_length=2)),
                ('in_time', models.CharField(blank=True, max_length=200, null=True)),
                ('out_time', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]