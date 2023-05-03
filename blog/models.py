from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.urls import reverse


class PostQuerySet(models.QuerySet):
    """
    Кастомный менеджер для модели Post.
    """

    def year(self, year):
        """
        Выборка по году.
        """

        posts_at_year = self.filter(published_at__year=year).order_by('published_at')
        return posts_at_year


class TagQuerySet(models.QuerySet):
    """
    Кастомный менеджер для модели Tag.
    """

    def popular(self):
        """
        Популярные тэги.
        """

        most_popular_tags = self.annotate(amount_tags=Count('posts')).order_by('-amount_tags')
        return most_popular_tags


class Post(models.Model):
    """
    Пост.
    """

    title = models.CharField(
        'Заголовок',
        max_length=200
    )
    text = models.TextField(
        'Текст'
    )
    slug = models.SlugField(
        'Название в виде url',
        max_length=200
    )
    image = models.ImageField(
        'Картинка'
    )
    published_at = models.DateTimeField(
        'Дата и время публикации'
    )
    author = models.ForeignKey(
        User,
        related_name='posts',
        verbose_name='Автор',
        limit_choices_to={'is_staff': True},
        on_delete=models.CASCADE
    )
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        verbose_name='Кто лайкнул',
        blank=True
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='posts',
        verbose_name='Теги'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    objects = PostQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('post_detail', args={'slug': self.slug})


class Tag(models.Model):
    """
    Тэг.
    """

    title = models.CharField(
        'Тег',
        max_length=20,
        unique=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    objects = TagQuerySet.as_manager()

    def clean(self):
        self.title = self.title.lower()

    def get_absolute_url(self):
        return reverse('tag_filter', args={'tag_title': self.slug})


class Comment(models.Model):
    """
    Комментарий.
    """

    post = models.ForeignKey(
        'Post',
        related_name='comments',
        verbose_name='Пост, к которому написан',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        'Текст комментария'
    )
    published_at = models.DateTimeField(
        'Дата и время публикации'
    )

    def __str__(self):
        return f'{self.author.username} under {self.post.title}'

    class Meta:
        ordering = ['published_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
