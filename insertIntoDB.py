# POKERSTARS HISTORY PARSER
#
import sys
import MySQLdb as mdb
import copy



def translateValues(value):
	'''translates a python variable to the database language'''
	if type(value)==str:
		val='\"'+value+'\"'
	elif type(value)==bool:
		val=int(value)
	elif value==None:
		val='NULL'
	else:
		val=value

	return val


def insertIntoTable(tableName,tableDict,connection):
	'''Inserts the pokerhand info contained in tableDict inside
	the database'''
	#insert the table
	#the trick is to name the colums like the dict keys
	#
	#
	#
	#BUILD THE SQL INPUT
	#
	execute_string='INSERT INTO '+tableName +' SET '
	for key,value in tableDict.iteritems():
		val=translateValues(value)
		execute_string+=key+'='+str(val)+', '
	#remove the last comma and extra space:
	execute_string=execute_string[:-2]
	execute_string+=';'
	#
	#
	print ''
	print 'the string is',execute_string
	print 
	#raw_input()
	#
	#
	cur=connection.cursor()
	cur.execute(execute_string)
	connection.commit()
	rows=cur.fetchall()
	for row in rows:
		print row

