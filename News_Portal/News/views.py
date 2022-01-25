from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    template_name = 'Posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostView(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'post'
