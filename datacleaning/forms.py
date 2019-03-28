from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Adress

class NewUserForm(UserCreationForm):
	STATUS_CHOICES = (
		("user", "user"),
		("company", "company"),
	)

	email = forms.EmailField(required=True)
	status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(), required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", "status")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class AdressForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AdressForm, self).__init__(*args, **kwargs)
		self.fields['company'].required = False
		self.fields['street'].required = False
		self.fields['city'].required = False
		self.fields['state'].required = False
		self.fields['zipc'].required = False
		self.fields['country'].required = False
	
	class Meta:
		model = Adress
		fields = ("company", "street", "city", "state", "zipc" ,"country")

	def save(self, commit=True):
		adress = super(AdressForm, self).save(commit=False)
		if commit:
			adress.save()
		return adress

class UploadFileForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(UploadFileForm, self).__init__(*args, **kwargs)
		self.fields['title'].required = False
		self.fields['file'].required = False
	title = forms.CharField(max_length=50)
	file = forms.FileField()