# Generated by Django 5.1.5 on 2025-01-17 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride_management_app', '0003_ride_ride_manage_pickup__2671db_idx_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='rideevent',
            index=models.Index(fields=['created_at'], name='ride_manage_created_b3cc96_idx'),
        ),
    ]
