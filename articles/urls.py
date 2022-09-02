from django.urls import path
from posts.views import PostsList, PostDetail, PostCreate, PostSearch, PostEdit, PostDelete


urlpatterns = [
   path('create/', PostCreate.as_view(), name='create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='edit.html'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='delete.html')
]