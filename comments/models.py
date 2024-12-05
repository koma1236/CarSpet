from django.db import models
from django.utils import timezone


class Comment(models.Model):
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, verbose_name="Автомобиль")
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return f'{self.author} - {self.car}: {self.content}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
