from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from accounts.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "error": "Email already exists."})
        password = attrs.get("password")
        attrs["password"] = make_password(password)
        attrs["username"] = attrs["email"]

        return attrs
