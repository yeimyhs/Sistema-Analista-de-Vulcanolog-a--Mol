from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Molecule(models.Model):
    id_mol = models.CharField(max_length=16)
    id = models.BigAutoField(primary_key=True)
    namemol = models.CharField(db_column='nameMol', max_length=128)  # Field name made lowercase.
    referencemol = models.CharField(db_column='referenceMol', max_length=128, blank=True, null=True)  # Field name made lowercase.
    yearrefmol = models.BigIntegerField(db_column='yearRefMol', blank=True, null=True)  # Field name made lowercase.
    kingdommol = models.CharField(db_column='kingdomMol', max_length=32)  # Field name made lowercase.
    genusmol = models.CharField(db_column='genusMol', max_length=32, blank=True, null=True)  # Field name made lowercase.
    speciemol = models.CharField(db_column='specieMol', max_length=64, blank=True, null=True)  # Field name made lowercase.
    smilemol = models.TextField(db_column='smileMol')  # Field name made lowercase.
    doimol = models.CharField(db_column='doiMol', max_length=64, blank=True, null=True)  # Field name made lowercase.
    journalmol = models.CharField(db_column='journalMol', max_length=512, blank=True, null=True)  # Field name made lowercase.
    classmol = models.CharField(db_column='classMol', max_length=128, blank=True, null=True)  # Field name made lowercase.
    statemol = models.IntegerField(db_column='stateMol', blank=True, null=True)  # Field name made lowercase.
    datecreationmol = models.DateTimeField(db_column='dateCreationMol')  # Field name made lowercase.
    lastmodificationmol = models.DateTimeField(db_column='lastModificationMol')  # Field name made lowercase.

    class Meta:
        db_table = 'Molecula'


class UserP(models.Model):
    id = models.OneToOneField(User,related_name='user_profile', on_delete=models.CASCADE, primary_key=True,unique=True)
    #id = models.BigAutoField( primary_key=True)  # Field name made lowercase.
    email = models.CharField( max_length=512)  # Field name made lowercase.
    password = models.CharField( max_length=64)  # Field name made lowercase.
    firstname = models.CharField(max_length=128)  # Field name made lowercase.
    lastname = models.CharField( max_length=128, blank=True, null=True)  # Field name made lowercase.
    imagecover = models.CharField(max_length=512, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(max_length=512, blank=True, null=True)  # Field name made lowercase.
    phone = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    username = models.CharField( max_length=128)  # Field name made lowercase.
    adress = models.CharField(max_length=512, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(max_length=512, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField( blank=True, null=True)  # Field name made lowercase.
    datecreation = models.DateTimeField()  # Field name made lowercase.
    type = models.IntegerField( default=0)  # Field name made lowercase.
    class Meta:
        db_table = 'User'
