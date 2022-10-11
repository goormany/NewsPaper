from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    raitingAuthor = models.BigIntegerField(default=0)

    def update_raiting(self):
        postRat = self.post_set.aggregate(postRating=Sum("raitingPost"))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum("raitingComment"))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.raitingAuthor = pRat*3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    News = "NW"
    Articles = "AR"

    POSITIONS = [
        (News, "Новость"),
        (Articles, "Статья")
    ]

    title = models.CharField(max_length=255)
    text = models.TextField()
    category_choice = models.CharField(max_length=2, choices=POSITIONS, default=Articles)
    dateCreation = models.DateTimeField(auto_now_add=True)
    raitingPost = models.SmallIntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    postCategory = models.ManyToManyField(Category, through="PostCategory")

    def like(self):
        self.raitingPost += 1
        self.save()

    def dislike(self):
        self.raitingPost -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:124]}...'


class PostCategory(models.Model):
    postTrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryTrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    textComment = models.CharField(max_length=128)
    DateCreation = models.DateTimeField(auto_now_add=True)
    raitingComment = models.SmallIntegerField(default=0)

    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.raitingComment += 1
        self.save()

    def dislike(self):
        self.raitingComment -= 1
        self.save()


