# Generated by Django 2.1.2 on 2018-11-12 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20181108_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=40, verbose_name='年龄'),
        ),
    ]
