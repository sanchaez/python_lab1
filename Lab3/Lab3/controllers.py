from .views import View
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

class AbstractController:

	table = ''
	model = ''

	def add(self, request):
		if self.model().add(request.GET):
			return HttpResponse(1)
		return HttpResponse(0)

	def get(self, request):
		return View(self.table + '.html', request, self.model.objects.all()).renderPage()

	def delete(self, request):
		self.model().remove(request.GET['id'])
		return HttpResponseRedirect('/' + self.table + '/')

class IndexController (AbstractController):

	def get(self, request):
		return View('index.html', request, []).renderPage()

class DepartmentsController (AbstractController):

	def __init__(self):
		self.table = 'departments'
		self.model = Departments

class ProductsController (AbstractController):

	def __init__(self):
		self.table = 'products'
		self.model = Products
	
class OrderersController (AbstractController):

	def __init__(self):
		self.table = 'orderers'
		self.model = Orderers

class ExtraditionController (AbstractController):

	def __init__(self):
		self.table = 'extradition'
		self.model = Cart

	def get(self, request):
		extr = self.model.objects.all(); id = -1; i = 0; count = len(extr); tmp = []
		for	row in extr:
			if id != row.cart_id:
				id = row.cart_id
				if i < count:
					tmp.append([cart for cart in extr[i:] if cart.cart_id == row.cart_id])
			i += 1
		return View(self.table + '.html', request, tmp).renderPage()

	def update(self, request):
		self.model.objects.filter(cart_id = request.GET['cart'], product_id = request.GET['product']).update(state = 1)
		return HttpResponseRedirect('/' + self.table + '/')
