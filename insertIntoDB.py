# POKERSTARS HISTORY PARSER
#
import sys
import MySQLdb as mdb
import copy





def InsertPokerHandIntoDB(tableName,parsedDict,connection):
	'''Inserts the pokerhand info contained in parsedDict inside
	the database'''
	#insert the table
	#the trick is to name the colums like the dict keys
	execute_string='INSERT INTO '+tableName +' SET '
	for key,value in parsedDict.iteritems():
		execute_string+=key+'='+str(value)+', '
	execute_string+=';'
	print 'the string is',execute_string
	cur=connection.cursor()
	cur.execute(execute_string)
	connection.commit()
	rows=cur.fetchall()
	for row in rows:
		print row

