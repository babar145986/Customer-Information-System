from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	name = models.CharField(max_length=120, null=True)
	phone = models.CharField(max_length=120, null=True)
	email = models.CharField(max_length=120, null=True)
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	profile_pic = models.ImageField(default='profile.jpg', null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=120)

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
		('Indoor' , 'Indoor'),
		('Out Door' , 'Out Door')
		)
	name = models.CharField(max_length=120)
	price = models.CharField(max_length=120)
	category = models.CharField(max_length=120, choices=CATEGORY)
	description = models.CharField(max_length=120, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name

class Order(models.Model):
	STATUS = (
		('Pending' , 'Pending'),
		('Out for delivery' , 'Out for delivery'),
		('Delivered' , 'Delivered')
		)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=120, null=True, choices=STATUS)






