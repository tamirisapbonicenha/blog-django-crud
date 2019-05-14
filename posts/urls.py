from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostView.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('posts/', views.Posts.as_view(), name='posts'),
    path('posts/search/', views.search_posts, name='search_posts'),
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
    path('post_update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    # path('category_create/', views.category_create, name='category_create'),
]