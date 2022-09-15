from tkinter import W
from urllib import request
from xml.dom import ValidationErr
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import PostForm
from .filters import PostFilter
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives, send_mail
from datetime import datetime
from django.contrib.auth.models import User
from accounts.models import UsersSubscriptions, SubscribeMail
from django.template.loader import render_to_string

class PostsList(ListView):
    model = Post
    ordering = 'pub_time'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context
    

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'create.html'
    permission_required = ('posts.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            path_info = self.request.META['PATH_INFO']
            if path_info == '/news/create/':
                post.post_type = 'NE'
            elif path_info == '/articles/create/':
                post.post_type = 'PA'
    
        post_title = self.request.POST['title']
        post_text = self.request.POST['text']
        categories_id = self.request.POST['categories']
        # for category_id in categories_id:
        subscriptions = UsersSubscriptions.objects.filter(category=categories_id)
        for subscription in subscriptions:
            mail = SubscribeMail(
                username = subscription.user.username,
                title = post_title,
                text =  post_text,
                first_name = subscription.user.first_name,
                last_name = subscription.user.last_name,
            )
            mail.save()

            html_content = render_to_string(
                'subscribe_create.html',
                {'mail': mail}
            )
            print(html_content)

            msg = EmailMultiAlternatives(
                subject=f'{mail.title}',
                body=f'{mail.text}',
                from_email='romanags@yandex.ru',
                to=[subscription.user.email],
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
        return super().form_valid(form) 

class PostSearch(PostsList):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'

class PostEdit(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'edit.html'
    permission_required = ('posts.change_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            pub_path = self.request.META['PATH_INFO']
            pub_type = pub_path.split('/')[1]
            if pub_type == 'articles' and self.object.post_type == 'PA' or pub_type == 'news' and self.object.post_type == 'NE':
                return super().form_valid(form)
            else:
                raise ValidationErr(f'Редактирование невозможно: путь {pub_path} не соответствует типу публикации {self.object.post_type}')

class PostDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('posts_list')
    permission_required = ('posts.delete_post')

    def form_valid(self, form):
        if self.request.method == 'POST':
            pub_path = self.request.META['PATH_INFO']
            pub_type = pub_path.split('/')[1]
            if pub_type == 'articles' and self.object.post_type == 'PA' or pub_type == 'news' and self.object.post_type == 'NE':
                return super().form_valid(form)
            else:
                raise ValidationErr(f'Удаление невозможно: путь {pub_path} не соответствует типу публикации {self.object.post_type}')