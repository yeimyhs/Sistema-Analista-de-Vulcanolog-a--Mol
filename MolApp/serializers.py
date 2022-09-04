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


class MoleculeSerializer(ModelSerializer):

    class Meta:
        model = Molecule
        depth = 2
        fields = '__all__'


class UserPSerializer(ModelSerializer):

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
        print("(+++++++++++++++++++++++++)")
        UserPf.datecreation=datetime.now()
        print(UserPf.datecreation)
        UserPf.save()
        print("(+++++++++++++++++++++++++-------------)")
        return UserPf
