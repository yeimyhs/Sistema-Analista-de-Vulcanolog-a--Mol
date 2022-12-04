from rest_framework.routers import SimpleRouter
from MolApp import views
from .views import *


from knox import views as knox_views


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf.urls import url, include
from django.urls import path, re_path
#from django.contrib.auth.views import password_reset, password_reset_done, password_reset_complete, password_reset_confirm
from django.contrib.auth import views as auth_views
from drf_yasg.utils import swagger_auto_schema


from django.conf import settings
from django.conf.urls.static import static
app_name = 'molApp'
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
   re_path(r'^swagger(<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('userbyToken/', UserAPI.as_view()),
    path('logout/',decorated_logout_view, name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),#cuando inicia sesion en varios browser y quiere salir de todos

   path('mailer/', mailer.as_view()),
    path('searchbyMolName/<str:args>/', searchbyMolName.as_view()),
    re_path(r'^sea/$', searchMolGeneral.as_view()),
    re_path(r'^userSearch/$', searchUser.as_view()),
    path('listFilters/', listFilters),
    path('exportMolecule/', views.exportMolecule),
    path('csvupMolecule/', views.csvup.as_view()),
   path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
router = SimpleRouter()

router.register(r'molecule', views.MoleculeViewSet, 'molecule')
router.register(r'userp', views.UserPViewSet, 'userp')

urlpatterns += router.urls
