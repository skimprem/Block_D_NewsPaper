from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from accounts.resources import POST_TYPE

class Author(models.Model):
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
        self._rating = 0
        for comment in Comment.objects.filter(user = self.user):
            self._rating += comment.rating

        for post in Post.objects.filter(author = Author.objects.get(user =self.user)):
            self._rating += post.rating * 3
            for comments_to_post in Comment.objects.filter(post = post):
                self._rating += comments_to_post.rating

        self.save()

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    paper = 'PA'
    news = 'NE'

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE, default=paper)
    pub_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255, default='Введите название')
    text = models.TextField(default='Введите содержание')
    _rating = models.IntegerField(default=0)

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = int(value) if value >=0 else 0
        self.save()

    def like(self):
        self._rating += 1
        self.save()
    
    def dislike(self):
        self._rating += -1
        self.save()
        
    def preview(self):
        return f'{self.text[0:124]}...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='Введите комментарий')
    pub_time = models.DateTimeField(auto_now_add=True)
    _rating = models.IntegerField(default=0)

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = int(value) if value >=0 else 0
        self.save()

    def like(self):
        self._rating += 1
        self.save()
    
    def dislike(self):
        self._rating += -1
        self.save()