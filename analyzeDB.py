import sys
import MySQLdb as mdb
import copy
from getConnectionToDB import *


def analyzeHands():
	'''makes queries on the db'''

	con=getConnectionToDataBase()
	with con:
		return con
	#
	#

	execute_string='SELECT '