from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    friends = models.ManyToManyField('User', blank=True)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="outgoing_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="incoming_requests", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_user', 'to_user'], name="unique_friend_request"),
        ]
