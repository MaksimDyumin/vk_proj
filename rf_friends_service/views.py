from enum import Enum

from django.shortcuts import render
from django.db import transaction

from rest_framework import views
from rest_framework.request import Request
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView, ListCreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from rf_friends_service.models import User, FriendRequest
from rf_friends_service.serializers import RegisterUserSerializer, UserFriendsListSerializer, FriendOutgoingRequestsSerializer, FriendIncomingRequestSerializer, UserFriendStatusSerializer
# Create your views here.


class HelloWorldView(views.APIView):
    def get(self, request, format=None):
        return Response('Hello world!')
    
    def post(self, request, format=None):
        return Response({'text': 'Hello world!', 'method': 'post', 'data': request.data})


class RegistrationView(CreateAPIView):
    """Регистрирует нового пользователя"""

    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer


class UserFriendsListView(ListAPIView):
    """
    Возвращает список друзей
    Url=user/friends/
    """
    # queryset = User.objects.all()
    serializer_class = UserFriendsListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friends.all()


class FriendStatus(str, Enum):
    FRIENDS = 'FRIENDS'
    INCOMING_REQUEST = 'INCOMING_REQUEST'
    OUTGOING_REQUEST = 'OUTGOING_REQUEST'
    NOT_FRIENDS = 'NOT_FRIENDS'


class UserFriendStatusView(RetrieveDestroyAPIView):
    """
    GET инфо o реквесте в друзья, DELETE удаляет из друзей пользователя c Pk
    Url=user/friends/<int:pk>
    """

    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        user_to_check = self.get_object()

        are_friends = user.friends.filter(pk=user_to_check.id).exists()
        has_incoming_request = user.incoming_requests.filter(from_user_id=user_to_check.id).exists()
        has_outgoing_request = user.outgoing_requests.filter(to_user_id=user_to_check.id).exists()
        
        messages = {
            FriendStatus.NOT_FRIENDS: 'Нет ничего!',
            FriendStatus.FRIENDS: 'Уже друзья!',
            FriendStatus.INCOMING_REQUEST: 'Есть входящая заявка!',
            FriendStatus.OUTGOING_REQUEST: 'Есть исходящая заявка!',
        }

        status = FriendStatus.NOT_FRIENDS
        if are_friends:
            status = FriendStatus.FRIENDS
        elif has_incoming_request:
            status = FriendStatus.INCOMING_REQUEST
        elif has_outgoing_request:
            status = FriendStatus.OUTGOING_REQUEST
        
        return Response({'message': messages[status], 'status': status})

    def perform_destroy(self, instance):
        with transaction.atomic():
            user = self.request.user
            user.friends.remove(instance)
            instance.friends.remove(user)
    

class FriendsIncomingRequestListView(ListAPIView):
    """
    GET возвращает список входящих заявок
    Url=user/friend_requests/incoming/
    """

    serializer_class = FriendOutgoingRequestsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.incoming_requests.all()


class FriendIncomingRequestView(DestroyAPIView, 
                                UpdateAPIView):
    """
    PUT принять заявку, DELETE отклонить заявку
    Url=user/friend_requests/incoming/<int:pk>/
    """

    permission_classes = [IsAuthenticated]
    serializer_class = FriendIncomingRequestSerializer

    def get_queryset(self):
        return self.request.user.incoming_requests.all()

    def perform_update(self, serializer):
        with transaction.atomic():
            user = self.request.user
            new_friend = serializer.instance.from_user
            user.make_friends(new_friend)
            serializer.instance.delete()


class FriendOutgoingRequestsView(ListCreateAPIView):
    """
    GET возвращает список исходящих заявок, POST отправляет заявку
    Url=user/friend_requests/outgoing/
    """
    queryset = FriendRequest.objects.all()
    serializer_class = FriendOutgoingRequestsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.outgoing_requests.all()
    
    def perform_create(self, serializer):
        with transaction.atomic():
            user = self.request.user
            to_user = serializer.validated_data['to_user']
            
            try:
                incoming_request = user.incoming_requests.filter(from_user=to_user).get()
                user.make_friends(to_user)
                incoming_request.delete()
            except FriendRequest.DoesNotExist:
                serializer.save()
                


class FriendOutgoingRequestView(DestroyAPIView):
    """
    DELETE отменяет заявку
    Url=user/friend_requests/outgoing/<int:pk>/
    """
    serializer_class = FriendOutgoingRequestsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.outgoing_requests.all()
