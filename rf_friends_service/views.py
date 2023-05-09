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


class UserFriendStatusView(RetrieveDestroyAPIView):
    """
    GET инфо o реквесте в друзья, DELETE удаляет из друзей пользователя c Pk
    Url=user/friends/<int:pk>
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserFriendStatusSerializer

    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_id_to_get_status = kwargs.get('pk')
        friends = user.friends.all().values()
        outgoing_requests = user.outgoing_requests.all().values()
        incoming_requests = user.incoming_requests.all().values()

        friends_ids = [x['id'] for x in friends]
        to_user_ids = [x['to_user_id'] for x in outgoing_requests]
        from_user_ids = [x['from_user_id'] for x in incoming_requests]

        if user_id_to_get_status in friends_ids:
            return Response({'message': 'Уже друзья!'})
        
        if user_id_to_get_status in from_user_ids:
            return Response({'message': 'Есть входящая заявка!'})
        
        if user_id_to_get_status in to_user_ids:
            return Response({'message': 'Есть исходящая заявка!'})
        
        return Response({'message': 'Нет ничего!'})
        

    def get_queryset(self):
        return self.request.user.friends.all()
    

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
            new_friend = serializer.instance.from_user
            self.request.user.friends.add(new_friend)
            self.request.user.save()
            new_friend.friends.add(self.request.user)
            new_friend.save()
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
            to_user_id = int(self.request.data['to_user'])
            to_user = User.objects.filter(id=to_user_id)
            to_user = to_user.get()
            incoming_requests = user.incoming_requests.all().values()

            from_user_ids = [x['from_user_id'] for x in incoming_requests]

            if to_user_id in from_user_ids:
                user.friends.add(to_user_id)
                user.save()
                to_user.friends.add(user.id)
                to_user.save()
                friend_request = FriendRequest.objects.filter(from_user_id=1, to_user_id=2)
                friend_request.delete()
            else:
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
