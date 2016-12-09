import MySQLdb as mdb;

def getConnect():
	return mdb.connect(host = '127.0.0.1', user = 'root', passwd = '', db = 'lab2DB')

def insert(table, fields, values):
	colnames = ''; colValues = ''; i = 0; count = len(fields)
	while i < count:
		colnames += '`' + fields[i] + '`, '
		colValues += "'" + values[i] + "', "
		i += 1
	connect = getConnect()
	cursor = connect.cursor()
	cursor.execute('SET NAMES `utf8`')
	cursor.execute('INSERT INTO ' + table + ' (' + colnames[:-2] + ') VALUES (' + colValues[:-2] + ')')
	cursor.close()
	closeConnection(connect)
	return cursor.lastrowid

def select(table, fields = '*', where = ''):
	connect = getConnect()
	cursor = connect.cursor()
	cursor.execute('SET NAMES `utf8`')
	cursor.execute('SELECT ' + fields + ' FROM ' + table + where)
	res = cursor.fetchall()
	cursor.close()
	closeConnection(connect)
	return res

def update(table, fields, values, where = ''):
	newValues = ''; i = 0; count = len(fields)
	while i < count:
		newValues += fields[i] + ' = ' + values[i] + ', '
		i += 1
	connect = getConnect()
	cursor = connect.cursor()
	cursor.execute('SET NAMES `utf8`')
	cursor.execute('UPDATE ' + table + ' SET ' + newValues[:-2] + where)
	cursor.close()
	closeConnection(connect)

def delete(table, where = ''):
	connect = getConnect()
	cursor = connect.cursor()
	cursor.execute('SET NAMES `utf8`')
	cursor.execute('DELETE FROM ' + table + where)
	cursor.close()
	closeConnection(connect)

def escapeBySymbol(str, sym):
	return sym + str + sym

def closeConnection(connection):
	connection.close()