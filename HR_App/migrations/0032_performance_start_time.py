# Generated by Django 5.0 on 2024-01-04 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0031_alter_performance_break_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
