from django.db import models
import uuid

# Create your models here.


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    bio = models.TextField()

    def __str__(self):
        return self.username


class Tweet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(
        User, related_name="liked_tweets", blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.CharField(max_length=140)
    tweet_id = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(
        User, related_name="liked_comments", blank=True)

    def __str__(self):
        return self.content
