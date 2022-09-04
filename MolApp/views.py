from rest_framework.viewsets import ModelViewSet
from MolApp.serializers import MoleculeSerializer, UserPSerializer
from MolApp.models import Molecule, UserP
#----------------------------------------------------------------------Register imports
from .serializers import RegisterSerializer , UserSerializer
from knox.models import AuthToken, User

from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
#----------------------------------------------------------------------Login imports
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
#----------------------------------------------------------------------token imports
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.http.response import JsonResponse
#----------------------------------------------------------------------swagger imports
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi
#https://drf-yasg.readthedocs.io/en/stable/custom_spec.html


class MoleculeViewSet(ModelViewSet):
    queryset = Molecule.objects.order_by('pk')
    serializer_class = MoleculeSerializer


class UserPViewSet(ModelViewSet):
    queryset = UserP.objects.order_by('pk')
    serializer_class = UserPSerializer


#----------------------------------------------------------------------Register

# Register API
class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
#----------------------------------------------------------------------Login
class LoginAPI(KnoxLoginView):
    
    permission_classes = (permissions.AllowAny,)
    @swagger_auto_schema( request_body=AuthTokenSerializer)

    def post(self, request, format=None):
        print(request)
        serializer = AuthTokenSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user.id)
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)



#----------------------------------------------------------------------service

      #bytoken

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserPSerializer
    def get_object(self):
        try :
            user = self.request.user
            print(user.id)
            queryset = UserP.objects.filter(id=user.id).first()
            print (queryset)
            return queryset
        except:
            return Response({'error': 'No se ha encontrado'})
