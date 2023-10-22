from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED
from rest_framework.authtoken.models import Token

from accounts.serializers import CreateUserSerializer
from profiles.serializers import ProfileSerializer, CreateProfileSerializer


# Create your views here.
class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({}, status=HTTP_204_NO_CONTENT)
        user_obj = serializer.validated_data['user']
        if not user_obj:
            return Response({}, status=HTTP_204_NO_CONTENT)
        profile_serializer = ProfileSerializer(instance=user_obj.profile, context={"request": request})

        token, created = Token.objects.get_or_create(user=user_obj)
        return Response({'token': token.key, 'profile': profile_serializer.data}, status=HTTP_200_OK)


class RegisterWithProfileCreateApiView(CreateAPIView):
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        data_obj = request.data.copy()
        user_serializer = CreateUserSerializer(data=data_obj)
        if not user_serializer.is_valid():
            return Response(
                user_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user_serializer:
            user = user_serializer.save()
        tp_data = dict(
            user=user.pk if user else None,
            **data_obj,
        )
        create_profile_serializer = CreateProfileSerializer(data=tp_data)
        if create_profile_serializer.is_valid():
            serializer_profile = create_profile_serializer.save()
        else:
            return Response(
                create_profile_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer_profile = ProfileSerializer(instance=serializer_profile, context={"request": request})
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'profile': serializer_profile.data}, status=HTTP_201_CREATED)