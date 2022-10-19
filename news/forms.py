from django import forms
from .models import *
from django.core.exceptions import ValidationError


class newsCreateForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            'title',
            'text',
            'author'
        ]


class articlesCreateForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            'title',
            'text',
            'author'
        ]
