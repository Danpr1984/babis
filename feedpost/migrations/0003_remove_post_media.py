# Generated by Django 3.2.15 on 2022-12-13 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("feedpost", "0002_alter_profile_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="media",
        ),
    ]