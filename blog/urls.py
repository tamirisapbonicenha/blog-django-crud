from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostView.as_view(), name='posts'),
    path('post/create', views.post_new, name='post_create'),
    path('post_detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('post_delete/<int:pk>/', views.post_delete, name='post_delete'),
]