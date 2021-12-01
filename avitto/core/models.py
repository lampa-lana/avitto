from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .validators import validate_date_edit, validate_birth_date
from django.urls import reverse
from django.template.defaultfilters import slugify


# Create your models here.


def user_foto_path(instance, filename):
    return 'user_{0}/foto/{1}'.format(instance.user.id, filename)


def user_directory_path(instance, filename):
    return 'user_{0}/posts/{1}'.format(instance.author.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name='пользователь')
    about = models.TextField(max_length=500, verbose_name='немного о себе')
    foto = models.ImageField(upload_to=user_foto_path,
                             verbose_name='фото пользователя')
    birth_date = models.DateField(
        null=True, blank=True, verbose_name='день рождения', validators=[validate_birth_date, ])
    post = models.ForeignKey(
        'Post', on_delete=models.PROTECT, null=True, blank=True, related_name='post', verbose_name='объявления пользователя')

    def __str__(self) -> str:
        return str(self.user.username)

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'список профилей пользователя'


class Category(models.Model):
    category_name = models.CharField(
        max_length=100, verbose_name='наименование категории', db_index=True)
    description = models.TextField(
        max_length=1000, blank=True, verbose_name='описание категории')
    # post = models.ManyToManyField(
    #     'Post', related_name='post_category',  verbose_name='объявления пользователя', blank=True)
    # author = models.ManyToManyField(
    #     'Profile',   related_name='author', verbose_name='автор объявления', blank=True)

    def __str__(self) -> str:
        return '{}'.format(self.category_name)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'список категорий'
        ordering = ['category_name']


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user', verbose_name='пользователь')
    post_name = models.CharField(
        max_length=100, verbose_name='наименование объявления')
    description = models.TextField(
        max_length=1000, blank=True, verbose_name='содержание объявления')
    image = models.ImageField(
        upload_to=user_directory_path, verbose_name='фотография товара')
    date_pub = models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания')  # (auto_now_add=True)
    date_edit = models.DateTimeField(
        auto_now=True, verbose_name='дата изменения', validators=[validate_date_edit])  # (auto_now=True)
    price = models.DecimalField(
        verbose_name='цена товара', max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, null=True, blank=True, related_name='category', verbose_name='категория товара')
    draft = models.BooleanField("Черновик", default=False)
    slug = models.SlugField(
        max_length=250, unique_for_date='date_pub')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self) -> str:
        return '(Пользователь {}: {},  цена: {})'.format(self.author.username, self.post_name, self.price, )

    # def get_absolute_url(self):
    #     return reverse('core:post_detail', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('core:post_detail', args=[str(self.id)])

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return '#'

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'список объявлений'
        # порядок сортировки с минусом в обратную сторону
        ordering = ['-category', '-date_pub']


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='пользователь')
    timestamp = models.DateTimeField(
        default=timezone.now, verbose_name='время')
    content = models.TextField(
        max_length=700, blank=False, verbose_name='содержимое')
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE, verbose_name='объявление')

    def __str__(self):
        return "{0} : {1}".format(self.user, self.content[:10] + "...")

    class Meta:
        verbose_name = 'комметарии'
        verbose_name_plural = 'список комментариев'
        ordering = ['-timestamp', ]

#
# def get_image_filename(instance, filename):
#     author = instance.post.author.id
#     name = instance.post.post_name
#     slug = slugify(name)
#     return 'user_{0}/posts/{1}/images{2}'.format(author, name, slug, filename)
#
#
# class Image(models.Model):
#     image = models.ImageField(
#         upload_to=get_image_filename, null=True, blank=True, verbose_name='изображение галереи')
#     post = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name="post_images", default=None, verbose_name='изображения к объявлению')
#
#     def __str__(self) -> str:
#         return '(Объявление {}: {} )'.format(self.post, self.image)
#
#     @property
#     def image_url(self):
#         if self.image and hasattr(self.image, 'url'):
#             return self.image.url
#         else:
#             return '#'
