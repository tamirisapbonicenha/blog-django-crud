from django.shortcuts import render,redirect
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

# def post_list(request):
#     return render(request, 'blog/post_list.html', {})

# class PostListView(View):
#     def get(self, request):
#         return render(request, 'blog/post_list.html', {})    

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

    
