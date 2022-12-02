from django.db import models
from django.contrib.auth.models import User
from accounts.models import Author 
from .resources import POST_TYPE
from django.urls import reverse
from django.core.cache import cache

class Category(models.Model):
    """
    Category: категории новостей/статей
    """
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f'{self.category_name}'

class Post(models.Model):
    """
    Post: модель содержит в себе статьи и новости
    author: o2m связь с моделью Author
    post_type: тип публикации - статья или новость
    put_time: автоматическая дата и время публикации
    categories: o2m связь с моделью Category
    title: заголовок
    text: текст
    _rating: рейтинг, который определяется количеством лайков
    like|dislike: методы, которые увеличивают/уменьшают рейтинг
    """
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

    def get_absolute_url(self):
        return reverse("post", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        # вызываем метод родителя, чтобы сохранился объект
        super().save(*args, **kwargs)
        # удаляем его из кэша, чтобы сбросить
        cache.delete(f'post-{self.pk}')
    
class PostCategory(models.Model):
    """
    PostCategory: промежуточная модель для m2m связи
    post: o2m связь с моделью Post
    category: o2m связь с моделью Category
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    """
    Comment: модель для комментариев к статье или новости
    post: o2m связь с моделью Post
    user: o2m связь с моделью User
    text: текст комментария
    put_time: дата и время публикации
    _rating: рейтинг, который определяется количеством лайков
    like|dislike: методы, которые увеличивают/уменьшают рейтинг
    """
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