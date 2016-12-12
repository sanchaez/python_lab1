from django.shortcuts import render

def index(request, pageData):
	return render(request, 'index.html', pageData)

def orders(request, pageData):
	return render(request, 'orders.html', pageData)

def orderers(request, pageData):
	return render(request, 'orderers.html', pageData)

def products(request, pageData):
	return render(request, 'products.html', pageData)

def departments(request, pageData):
	return render(request, 'departments.html', pageData)