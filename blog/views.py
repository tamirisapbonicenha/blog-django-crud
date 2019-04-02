from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import PostForm, PostEdit
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


def post_detail_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostEdit(request.POST or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        # return render(request, 'blog/post_detail.html', {'post': post})
        return redirect('post_detail', pk)

    context = {'form': form}
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

    
