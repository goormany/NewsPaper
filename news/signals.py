from django.db.models.signals import post_delete, pre_save, m2m_changed
from django.dispatch import receiver
import datetime
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, PostCategory


@receiver(post_delete, sender=Post)
def notify_managers_on_delete(sender, instance, **kwargs):
    subject = f"Пост с названием: {instance.title} был удален."

    mail_managers(
        subject=subject,
        message=f"Тип поста: {instance.category_choice}",
    )

    print(subject)


def send_notif(preview, pk, title, subscribers):
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'http://127.0.0.1:8000/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email="zarbot951@yandex.ru",
        to=subscribers
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_new_post_cateogry(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':

        categories = instance.postCategory.all()
        subscribers = []
        for category in categories:
            subscribers += category.subscribers.all()
        subscribers = [s.email for s in subscribers]

        send_notif(instance.preview(), instance.pk, instance.title, subscribers)
