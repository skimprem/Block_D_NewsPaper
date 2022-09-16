from tkinter import W
from xml.dom import ValidationErr
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from .filters import PostFilter
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
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