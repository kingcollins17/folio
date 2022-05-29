import profile
from rest_framework import views, status, permissions, generics
from knox.models import AuthToken
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.


class UserAPI(generics.RetrieveAPIView):

    serializer_class = UserSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user


class RegisterAPI(views.APIView):

    def post(self, request, *args, **kwargs):
        data = RegisterSerializer(data=request.data)
        if data.is_valid():
            user = data.save()
            token = AuthToken.objects.create(user)
            return Response(
                {
                    'user': UserSerializer(user).data,
                    'token': token[1]

                }, status=status.HTTP_201_CREATED
            )
        return Response('Oops!, invalid details provided', status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(views.APIView):
    """view for login"""

    def post(self, request, *args, **kwargs):
        data = LoginSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            if not data.validated_data == 'Invalid details':
                user = data.validated_data
                token = AuthToken.objects.create(user)

                return Response(
                    {
                        'user': UserSerializer(user).data,
                        'token': token[1]
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(data.validated_data, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(views.APIView):

    def get_object(self):
        try:
            return User.objects.all()[0]
        except User.DoesNotExist:
            return None

    def get(self, request):
        data = self.get_object()
        if data is not None:
            profile = data.profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Oops!, there is not content here', status=status.HTTP_204_NO_CONTENT)


class ProfileManageAPI(views.APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_pro(self, req_user):
        try:
            return ProfileInfo.objects.get(user=req_user)
        except ProfileInfo.DoesNotExist:
            return None

    def get(self, request):
        user = self.request.user
        profile = self.get_pro(user)
        if profile is not None:
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):

        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        instance = self.request.user.profile
        serializer = ProfileSerializer(instance, data=request.data)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        profile = self.request.user.profile
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
