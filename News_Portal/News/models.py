from django.contrib.auth.models import User
from django.db import models
from django.core.cache import cache
from django.urls import reverse


class Author(models.Model):
    author_name = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.author_name.username

    @property
    def update_rating(self):
        new_rating = (sum([post.rating_post * 3 for post in Post.objects.filter(author_post=self.author_name)])
            + sum([comment.rating_comment for comment in Comment.objects.filter(author_comment=self.author_name)])
            + sum([comment.rating_comment for comment in Comment.objects.filter(post__author_post=self.author_name)]))
        self.rating = new_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(
                                        User,
                                        through='Subscribe', related_name='subs'
                                        )

    def __str__(self):
        return self.name


# noinspection PyTypeChecker
class Post(models.Model):

    story = 'ST'
    news = 'NW'
    VARIANTS = [
        (story, 'статья'),
        (news, 'новость'),
    ]

    type = models.CharField(max_length=2, choices=VARIANTS)
    time = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating_post = models.IntegerField(default=0)
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    @property
    def preview(self):
        size = 124 if len(self.text) > 124 else len(self.text)
        return self.text[:size] + '...'

    @property
    def like(self):
        self.rating_post += 1
        self.save()

    @property
    def dislike(self):
        self.rating_post -= 1
        self.save()

    def get_absolute_url(self):
        return f'/posts/{self.pk}'

    def save(self, *args, **kwargs):        # для кэширования на низком уровне
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    author_comment = models.ForeignKey(Author, on_delete=models.CASCADE)
    rating_comment = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    @property
    def like(self):
        self.rating_comment += 1
        self.save()

    @property
    def dislike(self):
        self.rating_comment -= 1
        self.save()


class Subscribe(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub')
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.User.username}: {self.Category.name}'
