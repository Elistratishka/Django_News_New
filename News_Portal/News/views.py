from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    context_object_name = 'posts'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'News/Search.html'
    context_object_name = 'posts'
    ordering = ['-time']
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostAdd(CreateView):
    template_name = 'News/Add_news.html'
    form_class = PostForm


class PostEdit(UpdateView):
    template_name = 'News/Edit_news.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'News/Delete_news.html'
    queryset = Post.objects.all()
    success_url = '/posts/'
