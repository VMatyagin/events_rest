from core.auth_backend import PasswordlessAuthBackend
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from core.models import Position


class UserSerializer(serializers.ModelSerializer):
    """serializer for the users object"""

    brigades = serializers.SerializerMethodField('get_editable_brigades')

    def get_editable_brigades(self, obj):
        positions = Position.objects.filter(
            toDate__isnull=True, shtab__isnull=True, boec__vkId=obj.vkId
        ).values_list(
            'id', flat=True
        ).distinct()

        return positions

    # def get_past_seasons(self, obj):
    #     value_list = obj.seasons.values_list(
    #         'year', flat=True
    #     ).distinct()
    #     group_by_value = {}
    #     for value in value_list:
    #         list = obj.seasons.filter(
    #             year=value
    #         ).only('boec')
    #         serializer = SeasonSerializer(
    #             list, many=True, fields=('boec', 'id'))

    #         group_by_value[value] = serializer.data

    #     return group_by_value

    class Meta:
        model = get_user_model()
        fields = ('id', 'brigades')
        # extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """create a new user and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update a user and return it"""
        # password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        # if password:
        #     user.set_password(password)
        #     user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """serializer for the user authentication object"""
    vkId = serializers.IntegerField()
    # password = serializers.CharField(
    #     style={'input_type': 'password'},
    #     trim_whitespace=False
    # )

    def validate(self, attrs):
        """validate and authenticate the user"""
        vkId = attrs.get('vkId')
        # password = attrs.get('password')

        user = PasswordlessAuthBackend.authenticate(
            request=self.context.get('request'),
            vkId=vkId,
            # password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
