# Generated by Django 4.0.3 on 2022-05-15 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='verification_code',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Код подтверждения'),
        ),
    ]