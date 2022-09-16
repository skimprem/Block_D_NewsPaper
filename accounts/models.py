from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
# from posts.models import Category

class Author(models.Model):
    """
    Author: модель, содержащая объекты всех авторов
    user: связь o2o со встроенной моделью User
    update_rating: вычисление рейтинга пользователя
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0)

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = int(value) if value >=0 else 0
        self.save()
    
    def update_rating(self):
        from posts.models import Comment, Post
        self._rating = 0
        for comment in Comment.objects.filter(user = self.user):
            self._rating += comment.rating

        for post in Post.objects.filter(author = Author.objects.get(user =self.user)):
            self._rating += post.rating * 3
            for comments_to_post in Comment.objects.filter(post = post):
                self._rating += comments_to_post.rating
        self.save()

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'


class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

class UsersSubscriptions(models.Model):
    from posts.models import Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class SubscribeMail(models.Model):
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    text = models.TextField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # link = models.URLField(max_length=200)