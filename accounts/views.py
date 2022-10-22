from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news.models import *


class accountUserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'account_accountUpdateUserView.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('news_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        context['is_your_id'] = int(self.request.user.id)
        context['path'] = int(self.request.path.split('/')[-1])
        return context


@login_required
def set_me_author(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
        Author.objects.create(authorUser=user)

    return redirect('/news/')

