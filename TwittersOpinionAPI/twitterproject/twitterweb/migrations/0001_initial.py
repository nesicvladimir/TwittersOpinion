# Generated by Django 3.0.7 on 2020-06-14 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TweetModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='def', max_length=280)),
                ('username', models.CharField(max_length=200, null=True)),
                ('label', models.CharField(max_length=20, null=True)),
                ('score', models.FloatField(null=True)),
                ('created_at', models.CharField(max_length=255, null=True)),
                ('location', models.CharField(max_length=255, null=True)),
                ('lat', models.FloatField(null=True)),
                ('lng', models.FloatField(null=True)),
                ('country_code', models.CharField(max_length=5, null=True)),
                ('state_code', models.CharField(max_length=5, null=True)),
            ],
        ),
    ]
