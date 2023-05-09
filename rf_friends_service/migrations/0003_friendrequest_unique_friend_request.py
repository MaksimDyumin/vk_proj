# Generated by Django 4.2.1 on 2023-05-08 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rf_friends_service', '0002_user_friends_friendrequest'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='friendrequest',
            constraint=models.UniqueConstraint(fields=('from_user', 'to_user'), name='unique_friend_request'),
        ),
    ]
