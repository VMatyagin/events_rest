from core.auth_backend import PasswordlessAuthBackend
from core.models import Activity, Boec, Brigade, Position, Shtab
from core.serializers import DynamicFieldsModelSerializer
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status
from so.serializers import BoecInfoSerializer, BrigadeSerializer, ShtabSerializer


class UserSerializer(serializers.ModelSerializer):
    """serializer for the users object"""

    brigades = serializers.SerializerMethodField(
        "get_editable_brigades", read_only=True
    )
    seasonBrigades = serializers.SerializerMethodField(
        "get_season_brigades", read_only=True
    )
    shtabs = serializers.SerializerMethodField("get_editable_shtabs", read_only=True)
    boec = serializers.SerializerMethodField("get_boec", read_only=True)
    unreadActivityCount = serializers.SerializerMethodField(
        "get_boec_unreadActivityCount", read_only=True
    )

    def get_editable_brigades(self, obj):
        brigades = Brigade.objects.filter(
            positions__toDate__isnull=True, positions__boec__vkId=obj.vkId
        ).distinct()

        serializer = BrigadeSerializer(brigades, many=True, fields=("id", "title"))

        return serializer.data

    def get_season_brigades(self, obj):
        brigades = Brigade.objects.filter(seasons__boec__vkId=obj.vkId).distinct()

        serializer = BrigadeSerializer(brigades, many=True, fields=("id", "title"))

        return serializer.data

    def get_editable_shtabs(self, obj):

        shtabs = Shtab.objects.filter(
            positions__toDate__isnull=True,
            positions__boec__vkId=obj.vkId,
        ).distinct()

        serializer = ShtabSerializer(shtabs, many=True, fields=("id", "title"))

        return serializer.data

    def get_boec(self, obj):
        try:
            boec_obj = Boec.objects.get(vkId=obj.vkId)
            serializer = BoecInfoSerializer(boec_obj)
        except (Boec.DoesNotExist):
            msg = _("Boec not found")
            raise serializers.ValidationError({"error": msg})
        return serializer.data

    def get_boec_unreadActivityCount(self, obj):
        try:
            boec_obj = Boec.objects.get(vkId=obj.vkId)
            return boec_obj.unreadActivityCount
        except (Boec.DoesNotExist):
            msg = _("Boec not found")
            raise serializers.ValidationError({"error": msg})

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "brigades",
            "boec",
            "shtabs",
            "is_staff",
            "seasonBrigades",
            "unreadActivityCount",
        )

    def create(self, validated_data):
        """create a new user and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update a user and return it"""
        user = super().update(instance, validated_data)

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
        vkId = attrs.get("vkId")
        # password = attrs.get('password')

        user = PasswordlessAuthBackend.authenticate(
            request=self.context.get("request"),
            vkId=vkId,
            # password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authentication")

        attrs["user"] = user
        return attrs


class ActivitySerailizer(DynamicFieldsModelSerializer):
    """serializer for Activity"""

    class Meta:
        model = Activity
        fields = ("id", "type", "created_at", "warning")
