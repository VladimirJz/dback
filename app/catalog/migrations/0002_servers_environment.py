# Generated by Django 2.2 on 2021-11-26 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servers',
            name='Environment',
            field=models.SmallIntegerField(choices=[(1, 'Production'), (2, 'QA'), (3, 'Development')], default=1),
        ),
    ]