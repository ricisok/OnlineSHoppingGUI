# Generated by Django 4.2.7 on 2023-12-17 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mywb', '0006_remove_machine_alarm_remove_machine_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='example',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine', models.IntegerField(default='', max_length=100, verbose_name='机器号')),
                ('score', models.CharField(default='', max_length=100, verbose_name='分数')),
            ],
        ),
    ]
