from lab2 import selects as Select

def getTable(head, key, callback):
	return {'head': head, key: callback()}

def getNavigationBar():
	return [
		{'title': 'Orders', 'link': '/orders'},
		{'title': 'Orderers', 'link': '/orderers'},
		{'title': 'Products', 'link': '/products'},
		{'title': 'Departments', 'link': '/departments'}]


def getAllOrders():
	orders = Select.selectAllOrders(); res = []
	for order in orders:
		res.append({'id': order[0], 'data': [
			{'col': 'product', 'val': order[1]},
			{'col': 'count', 'val': order[2]},
			{'col': 'orderer', 'val': order[3] + ' ' + order[4]},
			{'col': 'cost', 'val': order[5]},
			{'col': 'terms', 'val': order[6]}]})
	return res
		

def getAllDepartments():
	departments = Select.selectAllDepartments()
	res = []
	for department in departments:
		res.append({'id': department[0], 'data': [{'col': 'department', 'val': department[1]}]})
	return res

def getAllProducts():
	res = []; products = Select.selectAllProducts()
	for product in products:
		res.append({'id': product[0], 'data': [{'col': 'product', 'val': product[1]},
												{'col': 'cost', 'val': product[2]},
												{'col': 'department', 'val': product[3]}]})
	return res

def getAllOrderers():
	orderers = Select.selectAllOrderers(); res = []
	for orderer in orderers:
		res.append({'id': orderer[0], 'data': [{'col': 'name', 'val': orderer[1]}, {'col': 'surname', 'val': orderer[2]}]})
	return res