from rest_framework.routers import SimpleRouter
from MolApp import views
from .views import *


from knox import views as knox_views


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf.urls import url, include
from django.urls import path 
#from django.contrib.auth.views import password_reset, password_reset_done, password_reset_complete, password_reset_confirm
from django.contrib.auth import views as auth_views
from drf_yasg.utils import swagger_auto_schema

schema_view = get_schema_view(
   openapi.Info(
      title="MolApp API",
      default_version='v0',
      description="-",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

decorated_logout_view = \
   swagger_auto_schema(
      'Authorization :: header for token authentication'
      #request_body={AuthTokenSerializer}
   )(knox_views.LogoutView.as_view())
urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/',decorated_logout_view, name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),#cuando inicia sesion en varios browser y quiere salir de todos

]
router = SimpleRouter()

router.register(r'molecule', views.MoleculeViewSet)
router.register(r'userp', views.UserPViewSet)

urlpatterns += router.urls
