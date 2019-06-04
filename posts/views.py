from django.http import Http404, HttpResponseNotAllowed, HttpResponse

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.views import View
from .forms import PostCreateForm, PostUpdateForm
from http.client import responses
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# CategoryForm
from .models import Post
from categories.models import Category


class PostView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        # context['most_visited'] = Post.objects.order_by('-visit_count')
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    # def get_object(self):
    #     object = super(PostDetail, self).get_object()
    #     object.add_visit()
    #     object.save()
    #     return object

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        response.set_cookie('post_%s' % self.object.id, True)
        # post_visited = request.COOKIES['post_1' % self.object.id]
        post_visited = request.COOKIES.get('post_%s' % self.object.id)

        if not post_visited:
            self.object.add_visit()
            self.object.save()

        return response


class Posts(ListView):
    template_name = 'posts/posts_all.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-id']



@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    template_name = 'posts/post_create.html'
    form_class = PostCreateForm
    success_url = '/posts/'
    model = Post

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context


class PostUpdateView(UpdateView):
    template_name = 'posts/post_update.html'
    form_class = PostUpdateForm
    success_url = '/posts/'
    model = Post

class PostDeleteView(DeleteView):
    template_name = 'posts/post_delete.html'
    model = Post
    success_url = '/posts/'

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
        'categories': Category.object.all()
    }

    return render(request, template, context)

