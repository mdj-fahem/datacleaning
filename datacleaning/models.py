from django.db import models
from django.contrib.auth.models import User

# Model Adress.
class Adress(models.Model):

	company = models.CharField(max_length=50, null=False, default="")

	street = models.CharField(max_length=100, null=True, default="")

	city = models.CharField(max_length=100, null=True, default="")
	
	state = models.CharField(max_length=100, null=True, default="")
	
	zipc = models.CharField(max_length=100, null=True, default="")
	
	country = models.CharField(max_length=50, null=True, default="")

	byScrapy = models.BooleanField(default=False)

	class Meta:
		verbose_name="Adress"
		ordering=['zipc']

	def __str__(self):
		return str(self.company)