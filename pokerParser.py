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
			actionID=0
			actionDict={}
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
		#process blinds

		if handState =='A':
			if 'posts' in line and 'blind' in line:
				part=line.partition(':')
				if part[1]!=':'
					print 'problem partitioning',line
				blindString=part[2]
				bwords=blindString.split()
				if not bwords[-1].isdigit():
					print 'problem parsing blinds'

				if 'small blind' in blindString:
						SB=float(bwords[-1])	
				elif 'big blind' in blindString:
						BB=float(bwords[-1])
				else:
					print 'problem parsing small blind'

		#
		#process the ANTE
		Ante=0.0
		if handState=='A'
			if 'posts the ante' in line:
				anteamount=line.split()[-1]
				if not anteamount.isdigit():
					print 'problem parsing the ante'
				else:	
					Ante+=float(line.split()[-1])
				#
			#
		#
		pokerTableDict['SB']=SB
		pokerTableDict['BB']=BB
		pokerTableDict['Ante']=Ante
		#
		#
		#process actions
		if handState in 'PFTR':
			semicln=line.find(':')
			if semicln != -1:
				testPlayerName=line[:semicln]
				if testPlayerName in playerNameList:
					#
					#
					#this is an action
					#
					#
					#
					if not actionDict:
						#initialize the action dictionary
						actionDict['pot']=pokerTableDict['SB']+pokerTableDict['BB']+pokerTableDict['Ante']
					#
					#
					#
					oldPot=actionDict['pot']
					actionDict=parseAction(line)
					if actionDict: #is not null so it was a valid action
						actionID+=1
						actionDict['actionID']=actionID
						actionDict['actionState']=handState
					#
					#
					#
					#
					#get the contribution to the pot from the action:
					if actionDict['action'] in ['bet','raise','call']:
						amount=actionDict['amount']
						assert amount!=None
						actionDict['pot']=oldPot+amount
					#
					#
					#
					#
					#
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
