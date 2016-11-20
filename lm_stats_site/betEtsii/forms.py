'''
Created on 15 jul. 2016

@author: mikamb93
'''
from django import forms
from betEtsii.models import Usuario


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
