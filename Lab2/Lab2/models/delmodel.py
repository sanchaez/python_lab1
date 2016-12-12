from lab2 import db as DataBase

def delete(table, id):
	DataBase.delete(DataBase.escapeBySymbol(table, "`"), where = 'WHERE `id` = ' + DataBase.escapeBySymbol(id, "'"))
	return 1