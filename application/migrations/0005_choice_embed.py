# Generated by Django 2.1.2 on 2018-12-30 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_auto_20181230_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='embed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Embed'),
        ),
    ]
