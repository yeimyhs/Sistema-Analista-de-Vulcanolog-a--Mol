from rest_framework.serializers import ModelSerializer
from MolApp.models import Molecule, UserP
from rest_framework import serializers
from django.contrib.auth.models import User

#-------------------------------
from datetime import datetime
# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserP
        fields = [ 
        'username', 
        'email' ,
        'password',
        'imagecover',
        'firstname',
        'lastname',
        'country',
        'phone',
        'adress',
        'city',
        'type'
        ]

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], 
            validated_data['email'], 
            validated_data['password'],
            )
        UserPf= UserP()                              
        UserPf.id =user
        UserPf.username = user.username
        UserPf.email = user.email
        UserPf.firstname = validated_data['firstname']
        UserPf.lastname = validated_data['lastname']
        UserPf.country = validated_data['country']
        UserPf.phone = validated_data['phone']
        UserPf.adress = validated_data['adress']
        UserPf.city = validated_data['city']
        UserPf.imagecover = validated_data['imagecover']
        UserPf.type = validated_data['type']
        UserPf.datecreation=datetime.now()
        print(UserPf.datecreation)
        UserPf.save()
        return user

# User Serializer
class UserSerializer(serializers.ModelSerializer):
   # user_profile = UserPSerializer(required=True)
    class Meta:
        model = User
        fields = (
        'id', 
        'username', 
        'email' ,
        )
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            )
        UserPf= UserP()
        UserPf.id =user
        UserPf.username = user.username
        UserPf.email = user.email
        UserPf.firstname = validated_data['firstname']
        UserPf.lastname = validated_data['lastname']
        UserPf.country = validated_data['country']
        UserPf.phone = validated_data['phone']
        UserPf.adress = validated_data['adress']
        UserPf.city = validated_data['city']
        UserPf.imagecover = validated_data['imagecover']
        UserPf.type = validated_data['type']
        UserPf.datecreation=datetime.now()
        print(UserPf.datecreation)
        UserPf.save()
        return user

from django.utils import timezone
class MoleculeSerializer(ModelSerializer):

    class Meta:
        model = Molecule
        depth = 2
        fields = '__all__'
        extra_kwargs = {
            'datecreationmol': {'read_only': True},
            'lastmodificationmol': {'read_only': True},
        }

    def create(self, validated_data):    
        idp = Molecule.objects.latest('pk')
        Molcre = Molecule.objects.create(      
            id= idp.pk+1,
            id_mol= validated_data['id_mol' ],
            namemol= validated_data['namemol' ],
            referencemol= validated_data['referencemol' ],
            yearrefmol= validated_data['yearrefmol' ],
            kingdommol= validated_data['kingdommol' ],
            genusmol= validated_data['genusmol' ],
            speciemol= validated_data['speciemol' ],
            smilemol= validated_data['smilemol' ],
            doimol= validated_data['doimol' ],
            journalmol= validated_data['journalmol' ],
            classmol= validated_data['classmol' ],
            statemol= validated_data['statemol' ],
            datecreationmol= timezone.now(),
            lastmodificationmol= timezone.now())
        return Molcre


class UserPSerializer(ModelSerializer):

    class Meta:
        model = UserP
        fields = [ 
        'id',
        'username', 
        'email' ,
        'imagecover',
        'firstname',
        'lastname',
        'country',
        'phone',
        'adress',
        'city',
        'type',
        'datecreation',
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'datecreation':{'read_only': True},
            'password': {'write_only': True}
            }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], 
            validated_data['email'], 
            validated_data['password'],
            )
        UserPf= UserP(id =user
        ,username = user.username
        ,email = user.email
        ,firstname = validated_data['firstname']
        ,lastname = validated_data['lastname']
        ,country = validated_data['country']
        ,phone = validated_data['phone']
        ,adress = validated_data['adress']
        ,city = validated_data['city']
        ,imagecover = validated_data['imagecover']
        ,type = validated_data['type']
        ,datecreation=datetime.now()) 
        UserPf.save()
        return UserPf


'''
anotaciones-------------------
            'id_mol',
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
            'classmol',
            'datecreationmol', 
            'lastmodificationmol',

                  validated_data['id_mol' ],
      validated_data['namemol' ],                    
      validated_data['referencemol' ],                    
      validated_data['yearrefmol' ],                    
      validated_data['kingdommol' ],                
      validated_data['genusmol' ],                    
      validated_data['speciemol' ],
      validated_data['smilemol' ],      
      validated_data['doimol' ],                
      validated_data['journalmol' ],
      validated_data['classmol' ],
      validated_data['statemol' ],
      validated_data['classmol' ],
'''