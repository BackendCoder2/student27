# Generated by Django 4.1.5 on 2023-01-15 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_submission_proof'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dfile',
            name='rfile',
        ),
        migrations.DeleteModel(
            name='RevInfo',
        ),
    ]
