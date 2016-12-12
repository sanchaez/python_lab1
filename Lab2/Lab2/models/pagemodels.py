from . import models
from lab2 import forms as Form

def index():
	return {'navbar': models.getNavigationBar()}

def orders():
	return {
		'navbar': models.getNavigationBar(),
		'table': models.getTable(['product', 'count', 'orderer', 'cost', 'terms', 'change/delete'], 'orders', models.getAllOrders),
		'forms': Form.getOrdersForms()}

def departments():
	return {
		'navbar': models.getNavigationBar(),
		'table': models.getTable(['department', 'change/delete'], 'departments', models.getAllDepartments),
		'forms': Form.getDepartmentsForms()}

def products():
	return {
		'navbar': models.getNavigationBar(),
		'table': models.getTable(['product', 'cost', 'department', 'change/delete'], 'products', models.getAllProducts),
		'forms': Form.getProductsForms()}

def orderers():
	return {
		'navbar': models.getNavigationBar(),
		'table': models.getTable(['name', 'surname', 'delete'], 'orderers', models.getAllOrderers),
		'forms': Form.getOrderersForms()}