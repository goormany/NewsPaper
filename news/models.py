from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
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

    def __str__(self):
        return f"{self.authorUser.username}"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author.authorUser.username}"

    def like(self):
        self.raitingPost += 1
        self.save()

    def dislike(self):
        self.raitingPost -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:124]}...'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):
    postTrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryTrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.postTrough}"


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


