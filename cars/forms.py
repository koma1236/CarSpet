from django import forms
from .models import Car


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите описание'}),
        }
        labels = {
            'make': 'Марка автомобиля',
            'model': 'Модель автомобиля',
            'year': 'Год выпуска',
            'description': 'Описание',
        }
        help_texts = {
            'make': 'Введите марку автомобиля.',
            'model': 'Введите модель автомобиля.',
            'year': 'Введите год выпуска автомобиля.',
        }
        error_messages = {
            'make': {
                'blank': 'Это поле не может быть пустым.',
            },
            'model': {
                'blank': 'Это поле не может быть пустым.',
            },
            'year': {
                'blank': 'Это поле не может быть пустым.',
                'invalid': 'Введите правильное число.',
            },
        }
