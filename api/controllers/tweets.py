from api.auth import BearerAuth
from ninja.pagination import paginate, LimitOffsetPagination
from uuid import UUID
from typing import List
from api.schemas import user, tweets
from ninja import Router
from ninja.errors import HttpError
from api import models

router = Router(tags=['tweets'])


@router.get("", response=List[tweets.TweetOut])
@paginate(LimitOffsetPagination)
def find_all(request):
    tweets = models.Tweet.objects.all()
    return tweets


@router.get("/{tweet_id}", response=tweets.TweetOut)
def find_one(request, tweet_id: UUID):
    tweet = models.Tweet.objects.get(id=tweet_id)
    return tweet


@router.post("", response=tweets.TweetOut, auth=BearerAuth())
def create(request, payload: tweets.TweetIn):
    user = models.User.objects.get(id=str(request.auth['id']))
    tweet = models.Tweet.objects.create(content=payload.content, user=user)

    return tweet


@router.patch("/{tweet_id}", response=tweets.TweetOut, auth=BearerAuth())
def update(request, tweet_id: UUID, payload: tweets.TweetIn):
    tweet = models.Tweet.objects.get(id=tweet_id)

    if not tweet.user.id == request.auth['id']:
        raise HttpError(401, "Unauthorized")

    tweet.content = payload.content
    tweet.save()

    return tweet


@router.delete("/{tweet_id}", auth=BearerAuth())
def delete(request, tweet_id: UUID):
    tweet = models.Tweet.objects.get(id=tweet_id)
    if not tweet.user.id == request.auth['id']:
        raise HttpError(401, "Unauthorized")
    tweet.delete()

    return {"message": "Tweet deleted successfully"}


@router.patch("/{tweet_id}/like", auth=BearerAuth(), response=tweets.TweetOut)
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


@router.patch("/{tweet_id}/unlike", auth=BearerAuth(), response=tweets.TweetOut)
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


@router.post("/{tweet_id}/comments", response=tweets.TweetOut, auth=BearerAuth())
def comment(request, tweet_id: UUID, payload: tweets.TweetIn):
    tweet = models.Tweet.objects.get(id=tweet_id)
    comment = models.Comment.objects.create(
        content=payload.content, tweet_id=tweet, user_id=request.auth)

    tweet.content = f"{tweet.content} {comment.content}"
    tweet.save()

    return tweet


@router.get("/{tweet_id}/comments", response=List[tweets.TweetOut])
@paginate(LimitOffsetPagination)
def get_comments(request, tweet_id: UUID):
    tweet = models.Tweet.objects.get(id=tweet_id)
    comments = models.Comment.objects.filter(tweet_id=tweet)

    return comments


@router.patch("/{tweet_id}/comments/{comment_id}", response=tweets.TweetOut, auth=BearerAuth())
def update_comment(request, tweet_id: UUID, comment_id: UUID, payload: tweets.TweetIn):
    tweet = models.Tweet.objects.get(id=tweet_id)
    comment = models.Comment.objects.get(id=comment_id)

    if not comment.user.id == request.auth['id']:
        raise HttpError(401, "Unauthorized")

    comment.content = payload.content
    comment.save()
    tweet.save()

    return tweet


@router.delete("/{tweet_id}/comments/{comment_id}", response=tweets.TweetOut, auth=BearerAuth())
def delete_comment(request, tweet_id: UUID, comment_id: UUID):
    tweet = models.Tweet.objects.get(id=tweet_id)
    comment = models.Comment.objects.get(id=comment_id)

    if not comment.user.id == request.auth['id']:
        raise HttpError(401, "Unauthorized")

    comment.delete()
    tweet.save()

    return tweet
