#
# POKERSTARS HISTORY PARSER
#
import sys
import MySQLdb as mdb
import copy
from parseAction import *
from insertIntoDB import *

def getConnectionToDataBase():
	con = mdb.connect('localhost', 'eliasron', '123123123', 'pokerstars');
	with con:
		return con

def extractHandIDFromLine(line):
	'''extracts the unique hand number from the input text'''
	words=line.split()
	handNumber=words[2]
	if handNumber[0] != '#':
		print 'GOT THE WRONG WORD IN extractHandFromLine'

	else:
		'striping the initial #'
		return handNumber[1:-1]
#
#
def setHandStateTo(state):
	'''sets the current state to the hand'''

def extractPlayerInfoFromLine(line):
	if line[0:4]!='Seat':
		print 'you fed the wrong line to extractPlayerInfoFromLine, idiot'
	words=line.split()
	playerNumber=words[1][:-1] #remove the semicolon
	if words[1][-1]!=':': print 'getting the wrong number player'
	playerName=words[2]
	playerStack=words[3][1:] #removing the parenthesis

	return {'playerNumber':playerNumber,'playerName':playerName,'playerStack':playerStack}

def parsePokerHands(tableName,handLines,connection):

	inFile=open('ejemplo.txt','r')
	handLines=inFile
	'''parses a pokerhand into a series of database entries'''

	parsedDict={}
	pokerTableDict={}
	for line in handLines:

		if 'PokerStars Hand' in line:
			newHand=True
			#send the previous record into the DB
			if len(parsedDict)!=0:
				InsertPokerHandIntoDB(tableName,parsedDict, connection)
			parsedDict.clear()
		else:
			newHand=False


		#determine the hand state (setup/preflop/flop/turn/river/showdown)
		if  newHand: 
			handState='A'
		elif '*** HOLE CARDS ***' in line:
			handState='P'
		elif '*** FLOP *** ' in line:
			handState='F'
		elif '*** TURN *** ' in line:
			handState='T'
		elif '*** RIVER *** ' in line:
			handState='R'
		elif '*** SHOW DOWN *** ' in line:
			handState='S'		
		pokerTableDict['handState']=handState
		#
		#
		#
		#get handID upon start
		if newHand:
			activePlayers=[]
			playerNameList=[]
			handID=extractHandIDFromLine(line)
			#print 'the hand number is',handID
			pokerTableDict['handID']=handID
		#
		#
		#
		#
		#obtain the name of the players and their info before the round
		if handState=='A':
			if  line[0:4]=='Seat':				
				playerInfo=extractPlayerInfoFromLine(line)
				activePlayers.append(copy.deepcopy(playerInfo))
				playerNameList.append(playerInfo['playerName'])
		#
		#
		#
		#
		#process action
		if handState in 'PFTR':
			semicln=line.find(':')
			if semicln != -1:
				testPlayerName=line[:semicln]
				if testPlayerName in playerNameList:
					#this is an action
					print 'this line corresponds to an action'
					print line
					actionDict=parseAction(line)
					parsedDict['actionDict']=copy.deepcopy(actionDict)
			#
		#
		#
		#
		#



#
#
#

if __name__=='__main__':
	a=''
	tableName='actions'
	connection=getConnectionToDataBase()
	print 'yo'
	parsePokerHands(tableName,a,connection)
