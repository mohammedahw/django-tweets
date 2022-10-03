from ninja import NinjaAPI
from . import models
from .schemas import user, tweets
from typing import List
from uuid import UUID

controller = NinjaAPI()


@controller.get("/tweets", response=List[tweets.TweetOut])
def find_all(request):
    tweets = models.Tweet.objects.all()
    return tweets


@controller.get("/tweets/{tweet_id}", response=tweets.TweetOut)
def find_one(request, tweet_id: UUID):
    tweet = models.Tweet.objects.get(id=tweet_id)
    return tweet


@controller.post("/tweets", response=tweets.TweetOut)
def create(request, payload: tweets.TweetIn):
    tweet = models.Tweet.objects.create(**payload.dict())
    return tweet


@controller.put("/tweets/{tweet_id}", response=tweets.TweetOut)
def update(request, tweet_id: UUID, payload: tweets.TweetIn):
    tweet = models.Tweet.objects.get(id=tweet_id)
    tweet.content = payload.content
    tweet.save()
    return tweet


@controller.delete("/tweets/{tweet_id}")
def delete(request, tweet_id: UUID):
    tweet = models.Tweet.objects.get(id=tweet_id)
    tweet.delete()
    return {"message": "Tweet deleted successfully"}


@controller.put("/tweets/{tweet_id}/like")
def like(request, tweet_id: UUID):
    tweet = models.Tweet.objects.get(id=tweet_id)
    for user in tweet.liked_by:
        if user.id == request.auth.id:
            return {"message": "You already liked this tweet"}
    tweet.likes += 1
    tweet.save()
    return tweet


@controller.put("/tweets/{tweet_id}/unlike")
def unlike(request, tweet_id: UUID):
    tweet = models.Tweet.objects.get(id=tweet_id)
    for user in tweet.liked_by:
        if user.id == request.auth.id:
            tweet.likes -= 1
            tweet.save()
            return tweet
    return {"message": "You haven't liked this tweet yet"}


@controller.get("/users", response=List[user.UserOut])
def find_all(request):
    users = models.User.objects.all()
    return users


@controller.get("/users/{user_id}", response=user.UserOut)
def find_one(request, user_id: UUID):
    user = models.User.objects.get(id=user_id)
    return user


@controller.post("/users", response=user.UserOut)
def register(request, payload: user.UserIn):
    user = models.User.objects.create(**payload.dict())
    return user


@controller.post("/users/login", response=user.UserOut)
def login(request, payload: user.UserIn):
    user = models.User.objects.get(
        email=payload.username, password=payload.password)
    return user


@controller.put("/users/{user_id}", response=user.UserOut)
def update(request, payload: user.UserIn):
    user = models.User.objects.get(id=user_id)
    user.save()
    return user


@controller.delete("/users/{user_id}", response=user.UserOut)
def delete(request, user_id: UUID):
    user = models.User.objects.get(id=user_id)
    user.delete()
    return user
