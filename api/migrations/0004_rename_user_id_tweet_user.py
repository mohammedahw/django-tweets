# Generated by Django 4.0.3 on 2022-10-08 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='user_id',
            new_name='user',
        ),
    ]