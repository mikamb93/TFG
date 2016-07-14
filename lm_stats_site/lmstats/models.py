from django.db import models
from enum import unique
from MySQLdb.constants.FLAG import NOT_NULL, AUTO_INCREMENT
from django.db.models.fields import Field

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
    fechapartido = models.DateTimeField(db_column='fechaPartido', blank=True, null=True)  # Field name made lowercase.
    horapartido = models.DateTimeField(db_column='horaPartido', blank=True, null=True)  # Field name made lowercase.
    equipo1 = models.CharField(max_length=45, blank=True, null=True)
    equipo2 = models.CharField(max_length=45, blank=True, null=True)
    porcentaje1 = models.FloatField(blank=True, null=True)
    porcentajex = models.FloatField(db_column='porcentajeX', blank=True, null=True)  # Field name made lowercase.
    porcentaje2 = models.FloatField(blank=True, null=True)
    categoria = models.CharField(max_length=45, blank=True, null=True)
    competicion = models.CharField(max_length=45, blank=True, null=True)
    resultado = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partido'


class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)  # Field name made lowercase.
    nick = models.CharField(max_length=15)
    contrasena = models.CharField(max_length=45,db_column='contraseña')
    nombre = models.CharField(max_length=45, blank=True, null=True)
    apellido = models.CharField(max_length=45, blank=True, null=True)
    apuestasrealizadas = models.CharField(db_column='apuestasRealizadas', max_length=45, blank=True, null=True)  # Field name made lowercase.
    apuestasacertadas = models.CharField(db_column='apuestasAcertadas', max_length=45, blank=True, null=True)  # Field name made lowercase.
    puntos = models.IntegerField(db_column='Puntos', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuario'

class Apuesta(models.Model):
    idapuesta = models.AutoField(primary_key=True)
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_idUsuario')  # Field name made lowercase.
    partido_idpartido = models.ForeignKey('Partido', models.DO_NOTHING, db_column='partido_idpartido')
    pronostico = models.CharField(max_length=45, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    acierto_fallo = models.IntegerField(db_column='acierto/fallo', blank=True, null=True)  # Field renamed to remove unsuitable characters.

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





class LmstatsComputer(models.Model):
    name = models.CharField(max_length=60)
    active = models.IntegerField()
    date_created = models.DateTimeField()
    host_group = models.ForeignKey('LmstatsHostgroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lmstats_computer'


class LmstatsHostgroup(models.Model):
    name = models.CharField(unique=True, max_length=60)
    active = models.IntegerField()
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'lmstats_hostgroup'


