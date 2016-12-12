from . import db as DataBase

def selectAllOrders():
	table =  '`orderers`, `products`, `orders`'
	fields = '`orders`.`id`, `products`.`product`, `orders`.`count`, `orderers`.`name`, `orderers`.`surname`, \
			 (`orders`.`count` * `products`.`cost`) AS `cost`, `orders`.`terms`'
	where =  'WHERE `orders`.`product` = `products`.`id` AND `orders`.`orderer` = `orderers`.`id`'
	return DataBase.select(table, fields, where)

def selectAllOrderers(_fields = '*', _where = ''):
	return DataBase.select(table = '`orderers`', fields = _fields, where = _where)

def selectAllProducts():
	table =  '`products`, `departments`'
	fields = '`products`.`id`, `product`, `cost`, `name` AS `department`'
	where =  'WHERE `products`.`department` = `departments`.`id`'
	return DataBase.select(table, fields, where)

def selectAllDepartments(where = ''):
	return DataBase.select(fields = '*', table = '`departments`', where = '')