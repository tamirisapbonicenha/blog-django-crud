from django.http import Http404, HttpResponseNotAllowed, HttpResponse

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.db.models import Q
from django.views import View
from .forms import PostForm, PostEdit
# CategoryForm
from .models import Post, Category

class PostView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context    

# def posts(request):
#     posts_list =  Post.objects.all()
#     paginator = Paginator(posts_list, 5)
#     page = request.GET.get('page')
#     posts = paginator.get_page(page)

#     return render(request, 'posts/posts_all.html', {'posts': posts})

class Posts(ListView): 
    template_name = 'posts/posts_all.html'
    model = Post
    context_object_name = 'posts'  # Default: object_list
    paginate_by = 10
    ordering = ['-id']
    # queryset = Post.objects.all()

    def get_ordering(self):
        """Return the field or fields to use for ordering the queryset."""
        return self.ordering    

    def get_paginate_by(self, queryset):
        return self.paginate_by        
        

class PostDetail(DetailView):
    # slug_field = 
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = 'Authors'
        return data

    # num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits'] = num_visits + 1    

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        if request.POST['title'] and request.POST['text'] and request.POST['category']:
            postEdit = Post.objects.get(pk=pk)
            print('#############', request.POST['category'])
            CategoryEdit = Category.objects.get(id=request.POST['category'])
            # postEdit = post
            postEdit.title = request.POST['title']
            postEdit.text = request.POST['text']
            postEdit.category = CategoryEdit
            postEdit.save()
            return redirect('post_detail', pk)
        else:
            return redirect('posts')

    context = {
        'post': post,
        'category': Category.objects.all()
    }

    return render(request, 'posts/post_edit.html', context)


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect('posts')

    return render(request, 'posts/post_delete.html', {'post': post})


# def post_delete_confirm(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.delete()
#     return redirect('posts')


# @login_required
# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.save()
#             return redirect('posts')
#     else:
#         form = PostForm()
#     return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_new(request):
    post = Post()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.author = form.cleaned_data['author']
            # bill = Bill.objects.get(form.cleaned_data['pk'])
            post.title = form.cleaned_data['title']
            post.text = form.cleaned_data['text']
            post.category = Category.objects.get(id=form.cleaned_data['category'])
            post.save()
    else:
        form = PostForm()

    return render(request, 'posts/post_create.html', {'form' : form})


# def category_create(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             c = Category(name=name)
#             c.save()
#     else:
#         form = CategoryForm()

#     return render(request, 'posts/category_create.html', {'form' : form})

def search_posts(request):
    template = 'posts/posts_all.html'  # padrões diferentes
    query = request.GET.get('q')
    results = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))

    context = {
        'posts': results,
    }

    return render(request, template, context)