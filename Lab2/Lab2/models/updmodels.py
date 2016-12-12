from lab2 import db as DataBase

def updDepartment(request):
	where = ' WHERE `id` = ' + DataBase.escapeBySymbol(request.GET['id'], "'")
	fields = [DataBase.escapeBySymbol('name', '`')]
	values = [DataBase.escapeBySymbol(request.GET['department'], "'")]
	DataBase.update(DataBase.escapeBySymbol('departments', '`'), fields, values, where)
	return	1

def updProduct(request):
	where = ' WHERE `id` = ' + DataBase.escapeBySymbol(request.GET['id'], "'")
	fields = [DataBase.escapeBySymbol('product', '`'), DataBase.escapeBySymbol('cost', '`')]
	values = [DataBase.escapeBySymbol(request.GET['product'], "'"),
				DataBase.escapeBySymbol(str(request.GET['cost']), "'")]
	DataBase.update(DataBase.escapeBySymbol('products', '`'), fields, values, where)
	return 1

def updOrder(request):
	product = DataBase.select(DataBase.escapeBySymbol('products', '`'),
							where = ' WHERE `product` = ' + DataBase.escapeBySymbol(request.GET['product'], "'"))
	if (len(product) == 0):
		return -1
	newCost = int(product[0][2]) * int(request.GET['count'])
	where = ' WHERE `id` = ' + DataBase.escapeBySymbol(request.GET['id'], "'")
	fields = [DataBase.escapeBySymbol('product', '`'),
				DataBase.escapeBySymbol('count', '`'),
				DataBase.escapeBySymbol('terms', '`')]
	values = [DataBase.escapeBySymbol(str(product[0][0]), "'"),
				DataBase.escapeBySymbol(str(request.GET['count']), "'"),
				DataBase.escapeBySymbol(request.GET['terms'], "'")]
	DataBase.update(DataBase.escapeBySymbol('orders', '`'), fields, values, where)
	return newCost