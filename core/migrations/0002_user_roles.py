# Generated by Django 4.0.3 on 2022-04-04 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.CharField(choices=[('user', 'Пользователь'), ('admin', 'Администратор')], default='user', max_length=5),
        ),
    ]
