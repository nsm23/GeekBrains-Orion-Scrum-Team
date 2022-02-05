from django.db import models
from django.conf import settings
from hub.models import Hub


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='Элиас для урла')
    text = models.TextField(verbose_name='Полный текст')
    brief_text = models.TextField(verbose_name='Сокращенный текст для списков')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='posts', verbose_name="Автор")
    hub = models.ForeignKey(Hub, null=True, blank=True, on_delete=models.SET_NULL, related_name='posts', verbose_name="Хаб")
    image = models.ImageField(upload_to='posts', null=True, blank=True, verbose_name='Картинка поста')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")

    def __str__(self):
        return self.title
