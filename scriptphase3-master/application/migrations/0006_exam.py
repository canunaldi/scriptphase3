# Generated by Django 2.1.2 on 2019-01-01 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_choice_embed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choices', models.ManyToManyField(related_name='choice', to='application.Choice')),
                ('q_embed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Embed')),
                ('q_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Topic')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Question')),
            ],
        ),
    ]
