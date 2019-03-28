from django.shortcuts import render, redirect
from datacleaning.models import Adress
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib import messages
from .forms import NewUserForm, AdressForm
from django.contrib.auth.decorators import login_required
from .utils import *
from .forms import UploadFileForm


# home.
def home(request):
	#Adress.objects.all().delete()
	#load_csv_adresses("ReferenceDB.csv")
	#adresses = Adress.objects.all().order_by('-id')[:10]
	form = AdressForm
	file_form = UploadFileForm()
	return render(request, 'datacleaning/home.html', locals())

# register new user
def register(request):
	if request.method == "POST" and register_form_is_valid(request):
		return home(request)
	form = NewUserForm
	return render(request, 'datacleaning/register.html', locals())

# connexion
def login_request(request):
	if request.method == "POST" and login_form_is_valid(request):
		return home(request)
	form = AuthenticationForm()
	return render(request, 'datacleaning/login.html', locals())

# déconnexion
@login_required
def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully !")
	return home(request)

# adress
@login_required
def adress(request):
	if request.method == 'POST':
			return checkAdress(request)
	return home(request)

@login_required
def checkAdress(request):
	if uploaded_file(request):
		adress = read_csv_adresses("input.csv")
		adresses, scores = matching(adress)
	else:
		adresses, scores = adress_form_is_valid(request=request, commit=False)
	if adresses:
		adresses_scores = zip(adresses, scores)
		return render(request, 'datacleaning/result.html', locals())
	return home(request)

# user account
@login_required
def account(request):
	return render(request, 'datacleaning/account.html')

# navbar search
@login_required
def search(request):
	adresses, scores = getAdressByCompany(request.POST.get('word'))
	adresses_scores = zip(adresses, scores)
	return render(request, 'datacleaning/result.html', locals())

def delete_account(request):
	request.user.delete()
	return logout_request(request)

# check adress
@login_required
def add_adress(request):
	adress_form_is_valid(request=request)
	return home(request)