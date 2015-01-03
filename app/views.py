# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, DetailView, UpdateView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from braces.views import LoginRequiredMixin
from models import User
from forms import EditMyProfileForm

class HomeView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all().order_by('?')[:16]
        context['user'] = self.request.user
        return context

class ProfileView(DetailView):
    template_name = "profile.html"
    model = User

class MyProfileView(LoginRequiredMixin, DetailView):
    template_name = "my-profile.html"
    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

class EditMyProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "edit-my-profile.html"
    fields = ['display_name', 'about', 'address', 'phone']
    success_message = 'Succesfully Saved.'
    def get_success_url(self):
        return reverse('my-profile', kwargs={})
    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)