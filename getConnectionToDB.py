

import MySQLdb as mdb

def getConnectionToDataBase():
	con = mdb.connect('localhost', 'eliasron', '123123123', 'pokerstars',charset='utf8');
	with con:
		return con