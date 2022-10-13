from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView


class newsListView(ListView):
    model = Post
    ordering = "-dateCreation"
    template_name = "news_newsListView.html"
    context_object_name = "newss"

class newsDetailView(DetailView):
    model = Post
    template_name = "news_newsDetailView.html"
    context_object_name = "news"
