from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.cache import cache


class PostList(ListView):
    model = Post
    context_object_name = 'posts'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


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


class PostAdd(PermissionRequiredMixin, CreateView):
    model = Post
    permission_required = ('News.add_post',)
    template_name = 'News/Add_news.html'
    form_class = PostForm


class PostEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    template_name = 'News/Edit_news.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post',)
    template_name = 'News/Delete_news.html'
    queryset = Post.objects.all()
    success_url = '/posts/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
        Author(author_name=user).save()
    return redirect('/posts')


@login_required
def subscribe_me(request):
    q = request.GET.get('q')
    user = request.user
    for i in q:
        try:
            user.subs.add(i)
        except:
            continue
    return redirect('/posts')
