from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from cars.models import Car
from cars.forms import CarCreateForm
from comments.models import Comment


class CarView(View):

    def get(self, request):
        cars = Car.objects.all()
        context = {
            'cars': cars
        }
        return render(request, 'cars.html', context=context)


class CarDetailView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        comments = Comment.objects.filter(car=car)
        context = {
            'car': car,
            'comments': comments
        }
        return render(request, 'car_detail.html', context=context)

    def post(self, request, pk):
        comment = request.POST.get('text')
        car = Car.objects.get(pk=pk)
        comments = Comment.objects.filter(car=car)
        context = {
            'car': car,
            'comments': comments
        }
        if comment is None:
            return JsonResponse({'status': 'error'})
        Comment.objects.create(content=comment, car=car, author=request.user)

        return render(request, 'car_detail.html', context=context)


class CreateCarView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def get(self, request):
        return HttpResponseRedirect(reverse('cars'))

    def post(self, request):
        car_create_form = CarCreateForm(data=request.POST)
        car_create_form.instance.owner = request.user
        if car_create_form.is_valid():
            car_create_form.save()
            return HttpResponseRedirect(reverse('cars'))

        return HttpResponseRedirect(reverse('cars'))


class DeleteCarView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def get(self, request):
        return HttpResponseRedirect(reverse('cars'))

    def post(self, request, pk):
        car = Car.objects.get(pk=pk)
        if request.user != car.owner:
            return JsonResponse({'status': 'error', 'data': 'Вы не можете удалить этот автомобиль'})
        car.delete()
        return HttpResponseRedirect(reverse('cars'), {'data': 'Автомобиль удален'})


class EditCarView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def get(self, request):
        return HttpResponseRedirect(reverse('cars'))

    def post(self, request, pk):
        car = Car.objects.get(pk=pk)
        if request.user != car.owner:
            return JsonResponse({'status': 'error', 'data': 'Вы не можете редактировать этот автомобиль'})
        car_edit_form = CarCreateForm(data=request.POST, instance=car)
        if car_edit_form.is_valid():
            car_edit_form.save()
            return HttpResponseRedirect(reverse('car-details', args=([pk]), ))
        return HttpResponseRedirect(reverse('car-details', args=([pk]), ))
