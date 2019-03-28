from .models import Adress
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, AdressForm, UploadFileForm
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 
import csv

# retourne les adresses de la company
def getAdressByCompany(word):
	adresses = list()
	scores = list()
	for adr in Adress.objects.all().order_by('-id'):
		score = fuzz.partial_ratio(adr.company, word)
		if score > 80:
			adresses.append(adr)
			scores.append(score)
	return adresses, scores

def login_form_is_valid(request):
	form = AuthenticationForm(request=request, data=request.POST)
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, f"Logged in successfully as : {username}")
			return True
	messages.error(request,"Invalid username or password")
	return False

def register_form_is_valid(request):
	form = NewUserForm(request.POST)
	if form.is_valid():
		user = form.save()
		username = form.cleaned_data.get('username')
		messages.success(request, f"New Account created : {username}")
		login(request, user)
		return True
	for msg in form.error_messages:
		messages.error(request, f"{msg}: {form.error_messages[msg]}")
	return False

def adress_form_is_valid(request, commit=True):
	form = AdressForm(request.POST)
	if form.is_valid():
		# récupération de l'adresse saisi par l'utilisateur
		newAdress = form.save(commit=False)
		messages.info(request, f"adresse de : {newAdress.company}")
		adresses, scores = matching(newAdress)
		# sauvegarder ou pas ?
		return adresses, scores
	return None, None

# si aucune adresse ne match elle retourne None
def matching(adresse):
	adresses = list()
	scores = list()
	for adr in Adress.objects.all().order_by('-id'):
		score = score_matching(adresse, adr)
		if score > 70:
			adresses.append(adr)
			scores.append(score)
	if len(adresses) > 0:
		return adresses, scores
	# sinon
	# faire du scraping ...
	#... sinon :
	return None, None

# renvoi le score de matching entre deux adresse
def score_matching(adress1, adress2):
	nb, score = 0,0
	if adress1.company and adress2.company:
		score = fuzz.token_sort_ratio(adress1.company, adress2.company)*5
		nb = 5
	if adress1.street and adress2.street:
		score += fuzz.partial_ratio(adress1.street, adress2.street)
		nb+=1
	if adress1.city and adress2.city:
		score += fuzz.partial_ratio(adress1.city, adress2.city)
		nb+=1
	if adress1.state and adress2.state:
		score += fuzz.partial_ratio(adress1.state, adress2.state)
		nb+=1
	if adress1.zipc and adress2.zipc:
		score += fuzz.partial_ratio(adress1.zipc, adress2.zipc)
		nb+=1
	if adress1.country and adress2.country:
		score += fuzz.partial_ratio(adress1.country, adress2.country)
		nb+=1
	if nb > 0:
		return score/nb
	return 0

# csv to database (Adresses)
def load_csv_adresses(path):
	with open(path) as f:
		reader = csv.reader(f)
		for row in reader:
			_, adress = Adress.objects.get_or_create(
				company=str(row[1]),
				street=str(row[2]),
				city=str(row[3]),
				state=str(row[4]),
				zipc=str(row[5]),
				country=str(row[6]),
				)

# csv to model (Adresses)
def read_csv_adresses(path):
	with open(path) as f:
		row = f.read().split(',')
		adress = Adress(
			company=str(row[1]),
			street=str(row[2]),
			city=str(row[3]),
			state=str(row[4]),
			zipc=str(row[5]),
			country=str(row[6]),
		)
	return adress

# upload file from form
def uploaded_file(request):
	form = UploadFileForm(request.POST, request.FILES)
	if form.is_valid():
		file = request.FILES.get('file')
		if request.POST.get('title'):
			#handle_uploaded_file(file)
			return True
	return False

def handle_uploaded_file(f):
	with open('input.csv', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def matching_multiple(adresses):
	return matching(adresses[0])