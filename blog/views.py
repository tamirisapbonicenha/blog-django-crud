from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import PostForm
from .models import Post

# Create your views here.
class PostView(View):
    def get(self, request):

        posts = Post.objects.all() 
        context = {
            'posts': posts
        }

        return render(request, 'blog/posts.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_delete(request, pk):
    if request.method == "POST":
        post = Post.objects.get(pk=pk).delete()
        return redirect('posts')
    else:
        post = Post.objects.get(pk=pk)
        return render(request, 'blog/post_delete.html', {'post': post})
    
    
def post_delete_confirm(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('posts')       


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

    
