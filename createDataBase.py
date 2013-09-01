#
#
#
import sys
import MySQLdb as mdb



def createTables():
	'''creates the test table if it doesn't exist'''

	con = mdb.connect('localhost', 'eliasron', '123123123', 'pokerstars');
	with con:
		cur=con.cursor()
		sqlstring='CREATE TABLE IF NOT EXISTS actions('
		sqlstring+='handID BIGINT, '
		sqlstring+='actionID SMALLINT,'
		sqlstring+='activePlayer VARCHAR(20), '		
		sqlstring+='handState VARCHAR(1), '
		sqlstring+='action VARCHAR(1), '
		sqlstring+='amount DECIMAL(6,2), '
		sqlstring+='pot DECIMAL(6,2), '
		sqlstring+='PRIMARY KEY(handID,actionID)'	
		sqlstring+=');'
		print sqlstring
		cur.execute(sqlstring)
		rows=cur.fetchone()
		print rows

		sqlstring='CREATE TABLE IF NOT EXISTS pokerHand('	
		sqlstring+='handID BIGINT, '
		sqlstring+='SB DECIMAL(6,2), '		
		sqlstring+='BB DECIMAL(6,2), '				
		sqlstring+='Ante DECIMAL(6,2), '	
		sqlstring+='SB_ID VARCHAR(20), '							
		sqlstring+='BB_ID VARCHAR(20), '									
		sqlstring+='DEALER_ID VARCHAR(20), '	
		sqlstring+='PRIMARY KEY(handID) '
		sqlstring+=');'
		print sqlstring
		cur.execute(sqlstring)
		rows=cur.fetchone()
		print rows






if __name__=='__main__':
	createTables()
