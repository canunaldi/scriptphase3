# Generated by Django 2.1.2 on 2019-01-01 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_auto_20190101_0147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='examid',
        ),
        migrations.AddField(
            model_name='exam',
            name='id',
            field=models.AutoField(auto_created=True, default=2, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
