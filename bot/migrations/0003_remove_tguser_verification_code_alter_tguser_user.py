# Generated by Django 4.0.3 on 2022-05-16 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bot', '0002_tguser_verification_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tguser',
            name='verification_code',
        ),
        migrations.AlterField(
            model_name='tguser',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь todolist'),
        ),
    ]
