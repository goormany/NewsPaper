from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum
from django.core.cache import cache


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    raitingAuthor = models.BigIntegerField(default=0, verbose_name='Рэйтинг автора')

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

    class Meta:
        verbose_name = ("Автор")
        verbose_name_plural = ("Авторы")


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название категории')
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Категория")
        verbose_name_plural = ("Категории")


class Post(models.Model):
    News = "NW"
    Articles = "AR"

    POSITIONS = [
        (News, "Новость"),
        (Articles, "Статья")
    ]

    title = models.CharField(max_length=255, verbose_name='Название поста')
    text = models.TextField( verbose_name='текст поста')
    category_choice = models.CharField(max_length=2, choices=POSITIONS, default=Articles, verbose_name='Тип поста')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание поста')
    raitingPost = models.SmallIntegerField(default=0, verbose_name='Рэйтинг поста')

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    postCategory = models.ManyToManyField(Category, through="PostCategory")

    def __str__(self):
        return f"ID: {self.id}, title: {self.title}, Author: {self.author.authorUser.username}"

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'news-{self.pk}')

    class Meta:
        verbose_name = ("Пост")
        verbose_name_plural = ("Посты")


class PostCategory(models.Model):
    postTrough = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    categoryTrough = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f"{self.postTrough}"

    class Meta:
        verbose_name = ("Пост с категориями")
        verbose_name_plural = ("Посты с категориями")


class Comment(models.Model):
    textComment = models.CharField(max_length=128, verbose_name='Текст комментария')
    DateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания комментария')
    raitingComment = models.SmallIntegerField(default=0, verbose_name='Рэйтинг комментария')

    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')

    def like(self):
        self.raitingComment += 1
        self.save()

    def dislike(self):
        self.raitingComment -= 1
        self.save()

    def __str__(self):
        return f'ID comment: {self.id}'

    class Meta:
        verbose_name = ("Комментарий")
        verbose_name_plural = ("Комментарии")


