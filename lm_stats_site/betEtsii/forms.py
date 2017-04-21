'''
Created on 15 jul. 2016

@author: mikamb93
'''
from django import forms
from django.contrib.auth.forms import UserCreationForm
import datetime as dt

from betEtsii.models import Usuario, AuthUser


class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = '__all__'
      
    #Validamos que el autor no sea menor a 3 caracteres
    def clean_usuario(self):
        diccionario_limpio = self.cleaned_data
    
        usuario = diccionario_limpio.get('usuario')
    
        if len(usuario) < 6:
            raise forms.ValidationError("El usuario debe contener mas de seis caracteres")
    
        return usuario

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)


    class Meta:
        model = AuthUser
        fields = ('username', 'email', 'password1', 'password2')        

    def save(self,commit = True):   
        user = super(UserCreationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True
        user.date_joined = dt.datetime.now()
        user.puntos = 0
        user.password = self.cleaned_data['password1']
        
        if commit:
            user.save()

        return user