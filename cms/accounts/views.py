from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import OrderFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.


def register(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)

			messages.success(request, "Account was created for " +username)

			return redirect('loginPage')

	context = {'form' : form}
	return render(request, 'accounts/register.html', context)


def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()
	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	myFilter = OrderFilter(request.GET, queryset = orders)
	orders = myFilter.qs
	context = {'myFilter' :myFilter, 'orders' : orders, 'total_order' : total_order, 'delivered' : delivered, 'pending' : pending}
	return render(request, 'accounts/user_page.html', context)


@login_required(login_url = 'login')
@admin_only
def home(request):
	all_customer = Customer.objects.all()
	all_order = Order.objects.all()
	total_order = all_order.count()
	delivered = all_order.filter(status = 'Delivered').count()
	pending = all_order.filter(status = 'Pending').count()
	context = {'all_customer' : all_customer, 'all_order' : all_order, 'total_order' : total_order,
				'delivered' : delivered, 'pending' : pending}
	return render(request, 'accounts/dashboard.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def customer_view(request, pk_test):
	customer = Customer.objects.get(id=pk_test)
	all_order = customer.order_set.all()
	total_order = all_order.count()
	delivered = all_order.filter(status = 'Delivered').count()
	pending = all_order.filter(status = 'Pending').count()
	myFilter = OrderFilter(request.GET, queryset = all_order)
	all_order = myFilter.qs
	context = {'myFilter' : myFilter, 'customer':customer,'all_order' : all_order, 'total_order' : total_order,'delivered' : delivered, 
				'pending' : pending}
	return render(request, 'accounts/customer.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def create_order(request):
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form' : form}
	return render(request, 'accounts/create_order.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk_test):
	order = Order.objects.get(id=pk_test)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form' : form}
	return render(request, 'accounts/create_order.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk_test):
	order = Order.objects.get(id=pk_test)
	order.delete()
	return redirect('/')


def logoutUser(request):
	logout(request)
	return redirect('loginPage')


def customer(request):
	return render(request, 'accounts/customer.html')

def product(request):
	return render(request, 'accounts/product.html')





