# Generated by Django 5.1.4 on 2025-01-17 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0010_attendance_posted_at_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('employee', 'Dipendente'), ('quality_manager', 'Quality Manager')], max_length=20),
        ),
    ]
