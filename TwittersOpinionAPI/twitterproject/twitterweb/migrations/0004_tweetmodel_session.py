# Generated by Django 3.0.7 on 2020-06-28 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitterweb', '0003_auto_20200614_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetmodel',
            name='session',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
