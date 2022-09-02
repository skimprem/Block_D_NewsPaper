from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostSearch, PostEdit, PostDelete


urlpatterns = [
   path('', PostsList.as_view(), name='posts_list'), 
   path('<int:pk>', PostDetail.as_view(), name='post'), 
   path('search/', PostSearch.as_view(), name='search'),
   path('create/', PostCreate.as_view(), name='create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='delete')
]