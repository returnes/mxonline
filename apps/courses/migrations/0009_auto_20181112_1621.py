# Generated by Django 2.1.2 on 2018-11-12 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20181110_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='教师'),
        ),
    ]
