from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, PostCategory, Category
import datetime


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


@shared_task
def notify_email_weeks():
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list("postCategory__name", flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    htlm_content = render_to_string(
        'week_notify.html',
        {
            'link': f'http://127.0.0.1:8000/',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email="zarbot951@yandex.ru",
        to=subscribers
    )
    msg.attach_alternative(htlm_content, 'text/html')
    msg.send()
