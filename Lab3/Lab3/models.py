from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Departments (models.Model):

	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 100)
	surname = models.CharField(max_length = 100)
	
	class Meta:
		db_table = 'departments'

	def add(self, data):
		department = Departments(name = data['name'], surname = data['surname'])
		department.save()
		return Departments.objects.latest('id')

	def remove(self, id):
		try:
			status = Cart.objects.get(cart = Extradition.objects.get(
				department = self.__class__.objects.get(id = id))).status
			if status:
				self.__class__.objects.filter(id = id).delete()
				return True
		except ObjectDoesNotExist:
			self.__class__.objects.filter(id = id).delete()
			return True
		return False

class Products (models.Model):
	
	id = models.IntegerField(primary_key = True)
	product = models.CharField(max_length = 100)
	department = models.ForeignKey(Departments, on_delete = models.CASCADE)
	
	class Meta:
		db_table = 'products'

	def add(self, data):
		product = Products(product = data['product'], department = data['department'])
		product.save()
		return Products.objects.latest('id')

	def remove(self, id):
		try:
			if Cart.objects.get(product_id = id).status:
				self.__class__.objects.filter(id = id).delete()
				return True
		except ObjectDoesNotExist:
			self.__class__.objects.filter(id = id).delete()
			return True
		return False
	
class Orderers (models.Model):

	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 100)
	surname = models.CharField(max_length = 100)
	
	class Meta:
		db_table = 'orderers'

	def add(self, data):
		orderer = Orderers(name = data['name'], surname = data['surname'])
		orderer.save()
		return Orderers.objects.latest('id')

	def remove(self, id):
		try:
			status = Cart.objects.get(cart__in = Extradition.objects.filter(orderer_id = id)).status
			if status:
				Orderers.objects.filter(id = id).delete()
				return True
		except ObjectDoesNotExist:
			Orderers.objects.filter(id = id).delete()
			return True
		return False

class Extradition (models.Model):

	id = models.IntegerField(primary_key = True)
	orderer = models.ForeignKey(Orderers, on_delete = models.CASCADE)
	product = models.ForeignKey(Products, on_delete = models.CASCADE)
	issued_date = models.CharField(max_length = 100)
	
	class Meta:
		db_table = 'extradition'

class Cart (models.Model):

	id = models.IntegerField(primary_key = True)
	cart = models.ForeignKey(Extradition, on_delete = models.CASCADE)
	product = models.ForeignKey(Products, on_delete = models.CASCADE)
	
	class Meta:
		db_table = 'cart'

	def add(self, data):
		try:
			Products = []
			for product in data.getlist('product[]'):
				Products.append(Products.objects.get(product = product))
			if len(Products) == 0:
				return False
			department = Departments.objects.get(name = data['d_name'], surname = data['d_surname'])
			orderer = Orderers.objects.get(name = data['o_name'], surname = data['o_surname'])
			Extradition(orderer = orderer, department = department, issued_date = data['date']).save()
			for product in Products:
				Cart(cart_id = Extradition.objects.latest('id').id, product = product).save()
			return Cart.objects.latest('id')
		except ObjectDoesNotExist:
			return False

	def remove(self, id):
		try:
			if Cart.objects.get(cart_id = id).status:
				self.__class__.objects.filter(id = id).delete()
				return True
		except ObjectDoesNotExist:
			self.__class__.objects.filter(id = id).delete()
			return True
		return False