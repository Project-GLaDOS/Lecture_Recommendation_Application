# Generated by Django 3.0.3 on 2020-02-28 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('user_email', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=15)),
                ('user_password', models.CharField(max_length=30)),
            ],
        ),
    ]