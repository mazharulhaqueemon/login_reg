from rest_framework import serializers

from accounts.models import User
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_user(self, obj):
        user_obj = obj.user
        try:
            return {
                'uid': user_obj.id,
                'email': user_obj.email
            }
        except:
            return {
                'uid': None,
                'email': None
            }


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "user",
            "full_name",
            "gender",
            "district",
            "division",
            "upozila"
        )
