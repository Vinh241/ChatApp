# Generated by Django 4.2 on 2023-04-16 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatapp", "0002_chatmessage"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatmessage",
            name="message_content",
            field=models.TextField(null=True),
        ),
    ]
