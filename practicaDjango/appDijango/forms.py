from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comentarios

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)
    
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		help_texts = {k:"" for k in fields }
  
  

class ComentarioForm(forms.ModelForm): 
	opinion = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':2, 'placeholder': '¿Qué estás pensando?'}), required=True)

	class Meta: #este es su copmportamiento 
		model = Comentarios
		fields = ['opinion']