# Generated by Django 4.0.3 on 2022-03-27 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieguessr', '0003_alter_usergame_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergame',
            name='score',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
