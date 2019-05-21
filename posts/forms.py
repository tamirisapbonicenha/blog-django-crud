from django import forms

from .models import Post, Author, Category

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'text', 'image', 'published']

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'text', 'image', 'published']