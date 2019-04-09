from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import PostForm, PostEdit
from .models import Post, Category

# Create your views here.
class PostView(View):
    def get(self, request):

        posts = Post.objects.all() 
        context = {
            'posts': posts
        }

        return render(request, 'blog/home.html', context)


def post_detail(request, pk):
    # post = get_object_or_404(Post, pk=pk)
    # return render(request, 'blog/post_detail.html', {'post': post})

    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
        
    return render(request, 'blog/post_detail.html', {'post': post})


def post_detail_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # print(postEdit)
    # form = PostEdit(request.POST or None, instance=post)

    if request.method == "POST":
        if request.POST['title'] and request.POST['text'] and request.POST['category']:
            postEdit = Post.objects.get(pk=pk)
            # CategoryEdit = Category.objects.get(pk=pk)
            # postEdit = post 
            postEdit.title = request.POST['title']
            postEdit.text = request.POST['text']
            # postEdit.category = request.POST['category']
            postEdit.save()
            return redirect('post_detail', pk)
        else: 
            return redirect('posts')

    context = {
        'post': post,
        'category': Category.objects.all()
    }

    return render(request, 'blog/post_detail_edit.html', context) 


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect('posts')
    
    return render(request, 'blog/post_delete.html', {'post': post})
    
    
# def post_delete_confirm(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.delete()
#     return redirect('posts')       


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('posts')
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})

    
