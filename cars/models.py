from django.db import models
from django.utils import timezone


class Car(models.Model):
    make = models.CharField(max_length=100, null=False, blank=False, verbose_name="Марка автомобиля")
    model = models.CharField(max_length=100, null=False, blank=False, verbose_name="Модель автомобиля")
    year = models.IntegerField(null=False, blank=False, verbose_name="Год выпуска")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Дата обновления")
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return f'{self.make} {self.model} {self.year}'

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-created_at']

