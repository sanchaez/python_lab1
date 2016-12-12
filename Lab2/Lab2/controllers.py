from django.http import HttpResponse
from . import views
from .models import delmodel as DelModel
from .models import addmodels as AddModels
from .models import updmodels as UpdModels
from .models import pagemodels as PageModels
import json

def fillDataBaseFromJSON(request):
	with open('lab2/static/db.json') as data_file:
		data = json.load(data_file)
		for item in data:
			for element in data[item]:
				if (AddModels.fillDataBaseWithJSONFile(item, list(element.keys()), list(element.values())) <= 0):
					return HttpResponse(0)
	return HttpResponse(1)

def orderAdd(request):
	return HttpResponse(json.dumps(AddModels.addOrder(request)))

def productAdd(request):
	return HttpResponse(AddModels.addProduct(request))

def departmentAdd(request):
	return HttpResponse(AddModels.addDepartment(request))

def ordererAdd(request):
	return HttpResponse(AddModels.addOrderer(request))


def index(request):
	return views.index(request, PageModels.index())

def orders(request):
	return views.orders(request, PageModels.orders())

def orderers(request):
	return views.orderers(request, PageModels.orderers())

def products(request):
	return views.products(request, PageModels.products())

def departments(request):
	return views.departments(request, PageModels.departments())


def orderUpdate(request):
	return HttpResponse(UpdModels.updOrder(request))

def productUpdate(request):
	return HttpResponse(UpdModels.updProduct(request))

def departmentUpdate(request):
	return HttpResponse(UpdModels.updDepartment(request))


def orderDelete(request):
	return HttpResponse(DelModel.delete('orders', request.GET.get('id')))

def productDelete(request):
	return HttpResponse(DelModel.delete('products', request.GET.get('id')))

def departmentDelete(request):
	return HttpResponse(DelModel.delete('departments', request.GET.get('id')))

def ordererDelete(request):
	return HttpResponse(DelModel.delete('orderers', request.GET.get('id')))