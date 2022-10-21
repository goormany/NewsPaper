from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class accountUserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'account_accountUpdateUserView.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('news_list')

