from django.db import models
from enum import unique
from MySQLdb.constants.FLAG import NOT_NULL, AUTO_INCREMENT
from django.db.models.fields import Field
from datetime import datetime
import betEtsii
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from betEtsii_site import settings


# Create your models here.

class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class Partido(models.Model):
    idpartido = models.AutoField(primary_key=True)
    fechapartido = models.DateField(db_column='fechaPartido', blank=True, null=True)  # Field name made lowercase.
    horapartido = models.TimeField(db_column='horaPartido', blank=True, null=True)  # Field name made lowercase.
    jornada = models.IntegerField(blank=True, null=True)
    equipo1 = models.CharField(max_length=45, blank=True, null=True)
    equipo2 = models.CharField(max_length=45, blank=True, null=True)
    porcentaje1 = models.FloatField(blank=True, null=True)
    porcentajex = models.FloatField(db_column='porcentajeX', blank=True, null=True)  # Field name made lowercase.
    porcentaje2 = models.FloatField(blank=True, null=True)
    competicion = models.CharField(max_length=45, blank=True, null=True)
    resultado = models.CharField(max_length=45, blank=True, null=True)
    resultadoreal = models.CharField(max_length=45, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'partido'
        
    def __str__(self):
        return self.equipo1 + ' - ' + self.equipo2 


class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)  # Field name made lowercase.
    nick = models.CharField(max_length=15)
    contrasena = models.CharField(max_length=45,db_column='contrasena')
    nombre = models.CharField(max_length=45, blank=True, null=True)
    apellido = models.CharField(max_length=45, blank=True, null=True)
    apuestasrealizadas = models.CharField(db_column='apuestasRealizadas', max_length=45, blank=True, null=True)  # Field name made lowercase.
    apuestasacertadas = models.CharField(db_column='apuestasAcertadas', max_length=45, blank=True, null=True)  # Field name made lowercase.
    puntos = models.IntegerField(db_column='Puntos', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return self.nick



class Apuesta(models.Model):

    
    
    
    idapuesta = models.AutoField(primary_key=True)
    usuario_idusuario = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='idusuario')  # Field name made lowercase.
    partido_idpartido = models.ForeignKey('Partido', models.DO_NOTHING, db_column='partido_idpartido')
    pronostico = models.CharField(max_length=45, blank=True, null=True)
    fecha = datetime.now().date()
    acierto_fallo = models.BooleanField(db_column='acierto/fallo', default=False)  # Field renamed to remove unsuitable characters.
    
    
    def __str__(self):
        return AuthUser.objects.get(idusuario=self.usuario_idusuario.idusuario).__str__() + ' : '+ Partido.objects.get(idpartido=self.partido_idpartido.idpartido).equipo1 +' '+ self.pronostico +' '+ Partido.objects.get(idpartido=self.partido_idpartido.idpartido).equipo2
        


    class Meta:
        managed = False
        db_table = 'apuesta'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class AuthUser(models.Model):
    REQUIRED_FIELDS = ('username','password')
    idusuario = models.CharField(max_length=128,db_column='id',primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    puntos = models.IntegerField()

    def __str__(self):
        return self.username
    
    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)




class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)




class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'



class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)

