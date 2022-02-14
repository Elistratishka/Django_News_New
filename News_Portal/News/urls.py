from django.urls import path
from .views import PostList, PostView, PostSearch, PostAdd, PostEdit, PostDelete, upgrade_me


urlpatterns = [
    path('', PostList.as_view(), name='list'),
    path('<int:pk>/', PostView.as_view(), name='detail'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
    path('search/', PostSearch.as_view(), name='search'),
    path('add/', PostAdd.as_view(), name='add'),
    path('upgrade/', upgrade_me, name='upgrade')
]
