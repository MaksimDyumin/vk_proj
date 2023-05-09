from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator

from rf_friends_service.models import User, FriendRequest


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
                'password': {
                    'style':{
                        'input_type': 'password'
                    },
                    'write_only': True
                }
            }

    def create(self, validated_data):
        ModelClass = self.Meta.model
        user = ModelClass.objects.create_user(validated_data['username'], password=validated_data['password'])
        return user
 

class UserFriendsListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [ 'id', 'username', 'friends']
        read_only_fields = ['users']


class FriendOutgoingRequestsSerializer(ModelSerializer):

    def validate_from_user(self, value):
        if self.context['request'].user.id != value.id:
            raise serializers.ValidationError("You must send friend_request from yourself only")
        return value

    def validate_to_user(self, value):
        if self.context['request'].user.id == value.id:
            raise serializers.ValidationError("You cant send friend_request to yourself")
        return value

    class Meta:
        model = FriendRequest
        fields = [ 'id', 'from_user', 'to_user']
        validators = [
                    UniqueTogetherValidator(
                        queryset=FriendRequest.objects.all(),
                        fields=['from_user', 'to_user']
                    )
                ]


class FriendIncomingRequestSerializer(ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = [ 'id', 'from_user', 'to_user']


class UserFriendStatusSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [ 'id', 'username', 'friends']