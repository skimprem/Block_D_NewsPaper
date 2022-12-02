from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostSearch, PostEdit, PostDelete
from django.views.decorators.cache import cache_page


urlpatterns = [
   # path('', cache_page(60)(PostsList.as_view()), name='posts_list'), 
   path('', PostsList.as_view(), name='posts_list'), 
   path('<int:pk>', cache_page(60 * 5)(PostDetail.as_view()), name='post'), 
   path('search/', PostSearch.as_view(), name='search'),
   path('create/', PostCreate.as_view(), name='create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='delete')
]