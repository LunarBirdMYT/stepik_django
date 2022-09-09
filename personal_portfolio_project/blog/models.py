from django.db import models

class Blog(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    description = models.TextField(verbose_name='Описание')
    created = models.DateField(verbose_name='Дата создания')

    def __str__(self) -> str:
        return self.title
