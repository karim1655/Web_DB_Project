# Generated by Django 5.1.4 on 2024-12-16 16:12
# Modified by me


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0005_alter_course_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Relazione',
            new_name='Attendance',
        ),
    ]
