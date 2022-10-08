from ninja import NinjaAPI

from . import models

from django.conf import settings


from .schemas import user, tweets

from typing import List

from uuid import UUID

from ninja.pagination import paginate, LimitOffsetPagination

from .auth import BearerAuth

import jwt

from ninja.errors import HttpError

from django.contrib.auth.hashers import make_password, check_password


controller = NinjaAPI()


@controller.get("/tweets", response=List[tweets.TweetOut])
@paginate(LimitOffsetPagination)
def find_all(request):

    tweets = models.Tweet.objects.all()
    return tweets


@controller.get("/tweets/{tweet_id}", response=tweets.TweetOut)
def find_one(request, tweet_id: UUID):

    tweet = models.Tweet.objects.get(id=tweet_id)
    return tweet


@controller.post("/tweets", response=tweets.TweetOut, auth=BearerAuth())
def create(request, payload: tweets.TweetIn):

    user = models.User.objects.get(id=str(request.auth['id']))

    tweet = models.Tweet.objects.create(
        content=payload.content, user=user)

    return tweet


@controller.patch("/tweets/{tweet_id}", response=tweets.TweetOut, auth=BearerAuth())
def update(request, tweet_id: UUID, payload: tweets.TweetIn):

    tweet = models.Tweet.objects.get(id=tweet_id)

    if not tweet.user.id == request.auth['id']:
        raise HttpError(401, "Unauthorized")

    tweet.content = payload.content

    tweet.save()
    return tweet


@controller.delete("/tweets/{tweet_id}", auth=BearerAuth())
def delete(request, tweet_id: UUID):

    tweet = models.Tweet.objects.get(id=tweet_id)
    if not tweet.user.id == request.auth['id']:
        raise HttpError(401, "Unauthorized")
    tweet.delete()

    return {"message": "Tweet deleted successfully"}


@controller.patch("/tweets/{tweet_id}/like", auth=BearerAuth(), response=tweets.TweetOut)
def like(request, tweet_id: UUID):

    tweet = models.Tweet.objects.get(id=tweet_id)
    if str(tweet.user.id) == request.auth['id']:
        raise HttpError(400, "you can't like your own tweet")

    is_liked = tweet.liked_by.filter(id=request.auth['id']).exists()

    if is_liked:
        raise HttpError(400, "you already liked this tweet")

    tweet.likes += 1
    tweet.liked_by.add(request.auth['id'])

    tweet.save()
    return tweet


@controller.patch("/tweets/{tweet_id}/unlike", auth=BearerAuth(), response=tweets.TweetOut)
def unlike(request, tweet_id: UUID):

    tweet = models.Tweet.objects.get(id=tweet_id)

    if str(tweet.user.id) == request.auth['id']:
        raise HttpError(400, "you can't unlike your own tweet")

    if not tweet.liked_by.filter(id=request.auth['id']).exists():
        raise HttpError(400, "you didn't like this tweet")

    tweet.likes -= 1
    tweet.liked_by.remove(request.auth['id'])
    tweet.save()
    return tweet


@controller.post("/tweets/{tweet_id}/comments", response=tweets.TweetOut, auth=BearerAuth())
def comment(request, tweet_id: UUID, payload: tweets.TweetIn):

    tweet = models.Tweet.objects.get(id=tweet_id)

    comment = models.Comment.objects.create(

        content=payload.content, tweet_id=tweet, user_id=request.auth)

    tweet.content = f"{tweet.content} {comment.content}"

    tweet.save()
    return tweet


@controller.get("/tweets/{tweet_id}/comments", response=List[tweets.TweetOut])
@paginate(LimitOffsetPagination)
def get_comments(request, tweet_id: UUID):

    tweet = models.Tweet.objects.get(id=tweet_id)

    comments = models.Comment.objects.filter(tweet_id=tweet)
    return comments


@controller.patch("/tweets/{tweet_id}/comments/{comment_id}", response=tweets.TweetOut, auth=BearerAuth())
def update_comment(request, tweet_id: UUID, comment_id: UUID, payload: tweets.TweetIn):

    tweet = models.Tweet.objects.get(id=tweet_id)

    comment = models.Comment.objects.get(id=comment_id)

    if not comment.user.id == request.auth['id']:
        raise HttpError(401, "Unauthorized")

    comment.content = payload.content

    comment.save()

    tweet.save()
    return tweet


@controller.delete("/tweets/{tweet_id}/comments/{comment_id}", response=tweets.TweetOut, auth=BearerAuth())
def delete_comment(request, tweet_id: UUID, comment_id: UUID):

    tweet = models.Tweet.objects.get(id=tweet_id)

    comment = models.Comment.objects.get(id=comment_id)
    if not comment.user.id == request.auth['id']:
        raise HttpError(401, "Unauthorized")
    comment.delete()

    tweet.save()
    return tweet


@controller.post("/users/login", response=user.LoginAndRegisterOut)
def login(request, payload: user.UserLoginIn):

    user = models.User.objects.get(

        username=payload.username)

    is_valid = check_password(payload.password, user.password)

    if not is_valid:

        raise HttpError(400, "invalid credentials")

    token_payload = {"id": str(user.id)}

    token = jwt.encode(token_payload, settings.SECRET_KEY,

                       algorithm="HS256")

    response = {"user": user, "token": token}

    return response


@controller.get("/users", response=List[user.UserOut])
@paginate(LimitOffsetPagination)
def find_all(request):

    users = models.User.objects.all()
    return users


@controller.get("/users/{user_id}", response=user.UserOut)
def find_one(request, user_id: UUID):

    user = models.User.objects.get(id=user_id)
    return user


@controller.post("/users", response=user.LoginAndRegisterOut)
def register(request, payload: user.UserRegisterIn):

    payload.password = make_password(password=payload.password)

    user = models.User.objects.create(**payload.dict())

    token_payload = {"id": str(user.id)}

    token = jwt.encode(token_payload, settings.SECRET_KEY,

                       algorithm="HS256")

    response = {"user": user, "token": token}
    return response


@controller.delete("/users/{user_id}", response=user.UserOut, auth=BearerAuth())
def delete(request, user_id: UUID):

    user = models.User.objects.get(id=user_id)
    if not user.id == request.auth['id']:
        raise HttpError(401, "Unauthorized")
    user.delete()
    return user
