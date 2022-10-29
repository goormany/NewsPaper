from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .models import *
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .filters import PostFilter
from .tasks import hello, printer
from django.urls import reverse_lazy
from .forms import newsCreateForm, articlesCreateForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class IndexView(View):
    def get(self, request):
        hello.delay()
        printer.delay(10)
        return HttpResponse('Hello!')


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
        post.author = Author.objects.get(authorUser=str(self.request.user.id))
        return super().form_valid(form)


class articlesCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = articlesCreateForm
    template_name = 'news_newsCreateView.html'
    permission_required = ('news.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_choice = "AR"
        post.author = Author.objects.get(authorUser=str(self.request.user.id))
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


class categoriesListView(ListView):
    model = Post
    template_name = 'news_categoriesListView.html'
    context_object_name = "categories_list"
    paginate_by = 10

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, pk=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['category'] = self.postCategory
        return context


@login_required
def add_me_to_category(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.add(user)

    # return redirect('categories_list', category)
    return redirect('/news/')