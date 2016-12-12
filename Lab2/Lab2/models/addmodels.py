from django.http import HttpResponse
from lab2 import db as DataBase
import re as RegExp

def fillDataBaseWithJSONFile(table, fields, values):
	return DataBase.insert(DataBase.escapeBySymbol(table, '`'), fields, values)

def addOrderer(request, flag = False):
	if (flag):
		if (not RegExp.match('\w{3,10}\s\w{3,10}', request.GET['orderer'])):
			return -1
		ordererName = request.GET['orderer'].split(' ')[0]
		ordererSurname = request.GET['orderer'].split(' ')[1]
	else:
		if (not RegExp.match('\w{3,10}\s\w{3,10}', request.GET['name'] + request.GET['surname'])):
			return -1
		ordererName = request.GET['name']
		ordererSurname = request.GET['surname']
	ordererWhere  = ' '.join(('WHERE `name` = ',
							DataBase.escapeBySymbol(ordererName, "'"),
							' AND `surname` = ',
							DataBase.escapeBySymbol(ordererSurname, "'")))
	orderer = DataBase.selectAllOrderers(where = ordererWhere)
	if (len(orderer) == 0):
		ordererId = DataBase.insert(DataBase.escapeBySymbol('orderers', "`"),
									['name', 'surname'], [ordererName, ordererSurname])
	else:
		ordererId = orderer[0][0]
	return ordererId

def addProduct(request):
	_where = ' '.join(('WHERE `product` = ', DataBase.escapeBySymbol(request.GET['product'], "'")))
	product = DataBase.select(DataBase.escapeBySymbol('products', '`'), where = _where)
	departmentId = addDepartment(request, flag = True)	
	if (len(product) != 0 or departmentId < 0):
		return -1
	return DataBase.insert(DataBase.escapeBySymbol('products', '`'),
							['product', 'cost', 'department'],
							[request.GET['product'], str(request.GET['cost']), str(departmentId)])

def addDepartment(request, flag = False):
	res = DataBase.select(DataBase.escapeBySymbol('departments', "`"),
							where = 'WHERE `name` = ' + DataBase.escapeBySymbol(request.GET['department'], "'"))
	if (len(res) == 0):
		return DataBase.insert(DataBase.escapeBySymbol('departments', '`'), ['name'], [request.GET['department']])
	if (flag):
		return res[0][0]
	return -1

def addOrder(request):
	_where = ' '.join(('WHERE `product` = ', DataBase.escapeBySymbol(request.GET['product'], "'")))
	product = DataBase.select(DataBase.escapeBySymbol('products', "`"), where = _where)
	orderer = addOrderer(request, True)
	if (len(product) == 0 or orderer <= 0):
		return {'res': -1}
	return {'res': DataBase.insert(DataBase.escapeBySymbol('orders', '`'),
							['product', 'count', 'orderer', 'terms'],
							[str(product[0][0]), str(request.GET['count']), str(orderer), request.GET['terms']]),
			'cost': int(product[0][2]) * int(request.GET['count'])}