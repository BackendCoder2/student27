# Generated by Django 4.1.5 on 2023-01-06 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_alter_job_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='state',
        ),
    ]
