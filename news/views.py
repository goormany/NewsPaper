from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .filters import PostFilter
from django.urls import reverse_lazy
from .forms import newsCreateForm, articlesCreateForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class newsListView(ListView):
    model = Post
    ordering = "-dateCreation"
    template_name = "news_newsListView.html"
    context_object_name = "newss"
    paginate_by = 10


class newsDetailView(DetailView):
    model = Post
    template_name = "news_newsDetailView.html"
    context_object_name = "news"


class newsSearchView(ListView):
    model = Post
    ordering = "-dateCreation"
    template_name = "news_newsSearchView.html"
    context_object_name = "newss"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class newsCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = newsCreateForm
    template_name = 'news_newsCreateView.html'
    permission_required = ('news.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_choice = "NW"
        return super().form_valid(form)


class articlesCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = articlesCreateForm
    template_name = 'news_newsCreateView.html'
    permission_required = ('news.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_choice = "AR"
        return super().form_valid(form)


class newsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = newsCreateForm
    template_name = 'news_newsCreateView.html'
    permission_required = ('news.change_post')


class articlesUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = newsCreateForm
    template_name = 'news_newsCreateView.html'
    permission_required = ('news.change_post')


class newsDeleteView(DeleteView):
    model = Post
    template_name = 'news_newsDeleteView.html'
    success_url = reverse_lazy('news_list')


class articlesDeleteView(DeleteView):
    model = Post
    template_name = 'news_newsDeleteView.html'
    success_url = reverse_lazy('news_list')

