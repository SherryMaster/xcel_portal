# Generated by Django 5.0 on 2023-12-22 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0022_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='minute',
        ),
    ]