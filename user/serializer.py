from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """ serializer from user model """

    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super(UserSerializer, self).update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return user


class TokenSerializer(serializers.Serializer):
    """ serializer class from generate token """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=True
    )

    def validate(self, attrs):
        """ overwrite method """
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
