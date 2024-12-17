# Generated by Django 5.1.4 on 2024-12-17 09:06

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0009_rename_stato_attendance_state_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='posted_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files_courses', to='web_app.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files_uploaded', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]