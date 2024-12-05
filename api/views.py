from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from cars.models import Car
from cars.serializers import CarSerializer
from comments.serializers import CommentSerializer
from comments.models import Comment


# Create your views here.

class CarDetail(APIView):
    def get_object(self, pk):
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        car = self.get_object(pk)
        if isinstance(car, Response):
            return car
        serializer = CarSerializer(car)
        return Response(serializer.data)

    def put(self, request, pk):
        car = self.get_object(pk)
        if isinstance(car, Response):
            return car
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        car = self.get_object(pk)
        if isinstance(car, Response):
            return car
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CarDetailViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentListView(APIView):
    def get(self, request, car_id):
        try:
            car = Car.objects.get(pk=car_id)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(car=car)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, car_id):
        try:
            car = Car.objects.get(pk=car_id)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(car=car, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
