# Generated by Django 5.1.4 on 2024-12-13 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='relazione',
            unique_together={('training_plan', 'user', 'stato')},
        ),
    ]