from django.urls import path
from . import views

urlpatterns = [
    # path('', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('post/create', views.post_new, name='post_create'),
    path('', views.PostView.as_view(), name='posts'),
]