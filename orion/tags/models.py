from django.db import models


class Tag(models.Model):
    text = models.CharField(max_length=32, verbose_name='Полный текст')

    def __str__(self):
        return self.text
