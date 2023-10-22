from django.urls import path

from accounts.views import CreateTokenView, RegisterWithProfileCreateApiView

urlpatterns=[
    path('token/',CreateTokenView.as_view()),
    path('register-with-profile-create/',RegisterWithProfileCreateApiView.as_view()),
]