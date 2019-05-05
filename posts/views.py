from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View
from .forms import PostForm, PostEdit
# CategoryForm
from .models import Post, Category

# Create your views here.
class PostView(View):
    def get(self, request):

        posts = Post.objects.all()
        context = {
            'posts': posts
        }

        return render(request, 'home.html', context)


def posts(request):
    posts_list =  Post.objects.all()
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'posts/posts_all.html', {'posts': posts})

def post_detail(request, slug):
    # post = get_object_or_404(Post, slug=slug)
    # return render(request, 'posts/post_detail.html', {'post': post})

    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    # post = Post.objects.filter(slug__iexact = slug)
    # if post.exists():
    #     post = post.first()
    # else:
    #     return HttpResponse('<h1>Post Not Found</h1>')

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'posts/post_detail.html', {'post': post, 'num_visits': num_visits,})


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