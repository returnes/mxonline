# Generated by Django 2.1.2 on 2018-11-10 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_video_learn_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseresource',
            old_name='lesson',
            new_name='course',
        ),
    ]
