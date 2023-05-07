from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rf_friends_service.models import User


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