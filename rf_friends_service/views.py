from django.shortcuts import render

from rest_framework import views
from rest_framework.generics import CreateAPIView 
from rest_framework.response import Response

from rf_friends_service.models import User
from rf_friends_service.serializers import RegisterUserSerializer
# Create your views here.


class HelloWorldView(views.APIView):
    def get(self, request, format=None):
        return Response('Hello world!')
    
    def post(self, request, format=None):
        return Response({'text': 'Hello world!', 'method': 'post', 'data': request.data})
    

class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer