from django.db import models

class Project(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    description = models.CharField(verbose_name='Описание', max_length=250)
    image = models.ImageField(verbose_name='Изображение', upload_to='portfolio/images')
    url = models.URLField(verbose_name='Ссылка', blank=True)

    def __str__(self):
        return self.title
