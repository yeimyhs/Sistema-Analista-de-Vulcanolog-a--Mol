from re import search
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
from .permissions import *
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

from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from MolApp.serializers import MoleculeSerializer, UserPSerializer
from MolApp.models import Molecule, UserP


from rest_framework.decorators import action
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *

fs = FileSystemStorage(location='tmp/')

class MoleculeViewSet(ModelViewSet):
    paginate_by = 10
    permission_classes = [IsAuthenticatedOrReadOnly,]
    queryset = Molecule.objects.order_by('id_mol')
    serializer_class = MoleculeSerializer
    def update(self, request, pk=None):
        try:
            item = Molecule.objects.get(pk=pk)
        except Molecule.DoesNotExist:
            return Response(status=404)
        serializer = MoleculeSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.lastmodificationmol= timezone.now()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UserPViewSet(ModelViewSet):
    paginate_by = 10
    queryset = UserP.objects.order_by('pk')
    serializer_class = UserPSerializer
    def destroy(self, request, pk=None):

        try:
            item = UserP.objects.get(pk=pk)
            item2 = User.objects.get(pk=pk)
        except UserP.DoesNotExist:
            return Response(status=404)
        item.delete()
        item2.delete()
        return Response(status=204)
    

'''
class MoleculeViewSet(ViewSet):
    #permission_classes = [postLog,]
    
    def list(self, request):
        queryset = Molecule.objects.order_by('namemol')
        serializer = MoleculeSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MoleculeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


    def retrieve(self, request, pk=None):
        queryset = Molecule.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = MoleculeSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Molecule.objects.get(pk=pk)
        except Molecule.DoesNotExist:
            return Response(status=404)
        serializer = MoleculeSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.lastmodificationmol= timezone.now()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
   
    def destroy(self, request, pk=None):
        try:
            item = Molecule.objects.get(pk=pk)
        except Molecule.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class UserPViewSet(ViewSet):
    
    def list(self, request):
        queryset = UserP.objects.order_by('pk')
        serializer = UserPSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = UserP.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = UserPSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = UserP.objects.get(pk=pk)
        except UserP.DoesNotExist:
            return Response(status=404)
        serializer = UserPSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.datecreation=datetime.now()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):

        try:
            item = UserP.objects.get(pk=pk)
        except UserP.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)
'''

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

#----------------------------------------------------------------------mailer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect

class mailer(APIView):
    permission_classes = [permissions.AllowAny, ]
    def post(self,request):
        #if request.method == "POST":
        #s="test laclolala final server"
        #m="test service api hci final server, ya salio :D"
        #e="verajulio823@gmail.com"
        subject= request.data["subject"]
        message= request.data["message"] + " " + request.data["email"]
        from_email= settings.EMAIL_HOST_USER
        recipient_list= request.data["email"]
        '''{
        "subject":"subject",
        "message":"message",
        "email":"email"
        }'''
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, [recipient_list])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            #return HttpResponseRedirect('/contact/thanks/')
            return HttpResponse('The email was send.')
        else:
            return HttpResponse('Make sure all fields are entered and valid.',request.data)

        #return Response(request, "contacto.html")


#----------------------------------------------------------------------------------servicios
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

from django.shortcuts import render
from rest_framework.permissions import AllowAny

class searchbyMolName(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    queryset =''
    @swagger_auto_schema(responses={200: MoleculeSerializer(many=True)},)
    def get(self,request,args):
        '''-description: search by Mol Name '''
        queryset = Molecule.objects.filter(namemol__icontains=args).order_by('id_mol')
        data = MoleculeSerializer(queryset, many=True).data
        return Response(data)

fieldsmol = ['namemol', 'smilemol','id_mol','speciemol','kingdommol','yearrefmol']
#https://www.django-rest-framework.org/api-guide/filtering/
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
class SmallPagesPagination(PageNumberPagination):  
    page_size = 10

class searchMolGeneral(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = SmallPagesPagination
    page_size = 10

    queryset = Molecule.objects.all().order_by('kingdommol','id_mol')
    serializer_class = MoleculeSerializer
    #filter_backends = []
    #filterset_fields = fieldsmol
    #filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    #search_fields = ['namemol', 'smilemol','id_mol','speciemol','kingdommol','yearrefmol']
    
    def post(self,request, format=None):
        #queryset=Q()
        query=Q()
        srchquery=Q()
        print(request.data)
        filters=["journalmol","yearrefmol","kingdommol","genusmol","speciemol","classmol"]
        
        for f in filters:
            if request.data["Filters"][f]:
                '''print (string)
                conditions = reduce(operator.and_, [Q(**{string: value}) for value in request.data["Filters"][f]])
                print(conditions)
                queryset+= Molecule.objects.filter(conditions)'''
                print(request.data["Filters"][f])
                
                for letter in request.data["Filters"][f]:
                    if "journalmol" == f:
                        query = query | Q(journalmol__icontains=letter)
                    elif "yearrefmol" == f:
                        query = query | Q(yearrefmol__icontains=letter)
                    elif "kingdommol" == f:
                        query = query | Q(kingdommol__icontains=letter)
                    elif "genusmol" == f:
                        query = query | Q(genusmol__icontains=letter)
                    elif "speciemol" == f:
                        query = query | Q(speciemol__icontains=letter)
                    elif "classmol" == f:
                        query = query | Q(classmol__icontains=letter)
        
        search= request.data["Search"]
        search = search.split(" ")
        print(search,"---------")
        for letter in search:
            srchquery = srchquery | Q(namemol__icontains=letter)| Q(yearrefmol__icontains=letter)| Q(smilemol__icontains=letter)| Q(id_mol__icontains=letter)| Q(kingdommol__icontains=letter)| Q(speciemol__icontains=letter)     
        print(srchquery)
        smtsearch = Molecule.objects.filter(srchquery).order_by(request.data["Orderby"],"id_mol")
        print(srchquery)
        usersWithPTRName = smtsearch.filter(query)
        data = MoleculeSerializer(usersWithPTRName, many=True).data
        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)
        
from django.db.models.functions import Lower
class searchUser(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    queryset = UserP.objects.all()
    serializer_class = UserPSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['username', 'email', 'lastname']
    ordering_fields = ['username', 'email', 'lastname']

#----------------------------------------------------------------csv export
#https://stackoverflow.com/questions/18685223/how-to-export-django-model-data-into-csv-file

import csv
from django.shortcuts import render
from django.http import HttpResponse
class csvup(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserPSerializer
    #@permission_classes((IsAuthenticated, ))
    def post(self, request):
        start_time = timezone.now()
        #file_path = options["file_path"]
        file = request.FILES["file"]

        content = file.read()  # these are bytes
        file_content = ContentFile(content)
        file_name = fs.save(
            "_tmp.csv", file_content
        )
        tmp_file = fs.path(file_name)
        file_path = tmp_file


        with open(file_path, "r") as csv_file:
            data = csv.reader(csv_file, delimiter=";")
            mols = []
            next(data)
            for row in data:
                idp = Molecule.objects.latest('pk')
                mol = Molecule(
                    id_mol=row[0],
                    id=idp.pk+1,
                    namemol=row[1],
                    classmol=row[2],
                    yearrefmol=row[3],
                    kingdommol=row[4],
                    genusmol=row[5],
                    speciemol=row[6],
                    smilemol=row[7],
                    doimol=row[8],
                    journalmol=row[9],
                    referencemol=row[10],
                    statemol=1,
                    datecreationmol=timezone.now(),
                    lastmodificationmol=timezone.now(),

                    )
                mols.append(mol)
                if len(mols) > 5000:
                    results = Molecule.objects.bulk_update_or_create(mols, ['id_mol',
                        'namemol',
                        'referencemol',
                        'yearrefmol',
                        'kingdommol',
                        'genusmol',
                        'speciemol',
                        'smilemol',
                        'doimol',
                        'journalmol',
                        'classmol',
                        'statemol',
                        'datecreationmol',
                        'lastmodificationmol'
                        ], match_field='id_mol')
                    mols = []
            if mols:
                results = Molecule.objects.bulk_update_or_create(mols, ['id_mol',
                    'namemol',
                    'referencemol',
                    'yearrefmol',
                    'kingdommol',
                    'genusmol',
                    'speciemol',
                    'smilemol',
                    'doimol',
                    'journalmol',
                    'classmol',
                    'statemol',
                    'datecreationmol',
                    'lastmodificationmol'
                    ], match_field='id_mol')
        end_time = timezone.now()
        
        return JsonResponse({'Results':results,"Time":{"Start":start_time,"End":end_time}})

@action(detail=False, methods=['GET'])
@permission_classes((IsAuthenticated, ))
def download_csv( request, queryset):
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    field_names =['id_mol',
                    'namemol',
                    'referencemol',
                    'yearrefmol',
                    'kingdommol',
                    'genusmol',
                    'speciemol',
                    'smilemol',
                    'doimol',
                    'journalmol',
                    'classmol'
                    ]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
download_csv.short_description = "Download selected as csv"

#por defecto necesita token (logueo)
def exportMolecule(request):
    data = download_csv(request, Molecule.objects.all())

    return HttpResponse (data, content_type='text/csv')

def listFilters(self):

    journal = [i for i in Molecule.objects.values_list('journalmol',flat=True).distinct()]
    year = [i for i in Molecule.objects.values_list('yearrefmol',flat=True).distinct()]
    kingdom = [i for i in Molecule.objects.values_list('kingdommol',flat=True).distinct()] 
    genus = [i for i in Molecule.objects.values_list('genusmol',flat=True).distinct()] 
    specie = [i for i in Molecule.objects.values_list('speciemol',flat=True).distinct()]
    classs = [i for i in Molecule.objects.values_list('classmol',flat=True).distinct()]
    return JsonResponse({"Filters":{'journal':journal,
    'year':year,
    'kingdom':kingdom,
    'genus':genus,
    'specie':specie,
    'class':classs}})
#propuesta con link https://stackoverflow.com/questions/25203259/django-filter-multiple-url-parameters
#
import operator
from functools import reduce
#https://stackoverflow.com/questions/5783588/django-filter-on-same-option-with-multiple-possibilities
from django.db.models import Q
class molFilterSearch(APIView):
    permission_classes = [permissions.AllowAny, ]
    def post(self,request, format=None):
            #queryset=Q()
            query=Q()
            print(request.data)
            filters=["kingdommol"]
            
            for f in filters:
                if request.data["Filters"][f]:
                    '''print (string)
                    conditions = reduce(operator.and_, [Q(**{string: value}) for value in request.data["Filters"][f]])
                    print(conditions)
                    queryset+= Molecule.objects.filter(conditions)'''
                    print(request.data["Filters"][f])
                    
                    for letter in request.data["Filters"][f]:
                        if "journalmol" == f:
                            query = query | Q(journalmol__icontains=letter)
                        elif "yearrefmol" == f:
                            query = query | Q(yearrefmol__icontains=letter)
                        elif "kingdommol" == f:
                            query = query | Q(kingdommol__icontains=letter)
                        elif "genusmol" == f:
                            query = query | Q(genusmol__icontains=letter)
                        elif "speciemol" == f:
                            query = query | Q(speciemol__icontains=letter)
                        elif "classmol" == f:
                            query = query | Q(classmol__icontains=letter)
                        print("==================================")
                        print(query)
                        
                    usersWithPTRName = Molecule.objects.filter(query)
                    
                    #print(usersWithPTRName)
            data = MoleculeSerializer(usersWithPTRName, many=True).data
            return Response(data)

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Molecule App"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]

    )