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
		return int(handNumber[1:-1])
#
#
def setHandStateTo(state):
	'''sets the current state to the hand'''

def extractPlayerInfoFromLine(line):
	'''extracts all the info about the player from the line'''
	#
	#
	if line[0:4]!='Seat':
		print 'you fed the wrong line to extractPlayerInfoFromLine, idiot'
	words=line.split()
	playerNumber=words[1][:-1] #remove the semicolon
	if words[1][-1]!=':': print 'getting the wrong number player'
	semicln=line.find(':')
	parenth=line.find('(')
	if not line.find('in chips'):
		print 'the extractPlayerInfo is not going to work, wrong line'
		assert False
	#
	playerName=line[semicln+2:parenth-1]
	#
	playerStackLine=line[parenth+1:]
	playerStackWords=playerStackLine.split()
	if (not playerStackWords[0].isdigit()) or playerStackWords[2]!='chips)':
		print 'the stack is not a number! or wrong line!'
		print 'the line is+',playerStackLine
		assert False
	else:
		playerStack=float(playerStackWords[0])

	return {'playerNumber':playerNumber,'playerName':playerName,'playerStack':playerStack}




#===================================================
#  PARSE THE POKERHANDS
#===================================================
def parsePokerHands(tableName,handLines,connection):

	'''parses the info inside of line'''
	inFile=open('ejemplo.txt','r')
	handLines=inFile
	'''parses a pokerhand into a series of database entries'''

	parsedDict={}
	pokerTableDict={}
	oldLine=''


	for line in handLines:




		if 'PokerStars Hand' in line:
			newHand=True
			#
			#
			#send the previous record into the DB
			#verbose=True;
			if pokerTableDict:
				insertIntoTable('pokerHand',pokerTableDict,connection)
			#
			#
			#
			parsedDict.clear()
			actionID=0
			actionDict={}
			SB=None
			BB=None
			Ante=None
			anteSum=0.0
			POT=0.0
			DEALER_ID=None
			SB_ID=None
			BB_ID=None			
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
		elif '*** SUMMARY ***' in line:
			handState='Y'		

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
				#print 'appending',playerInfo['playerName']
		#
		#
		#
		#
		#process blinds
		if handState =='A':
			if 'posts' in line and 'blind' in line:
				part=line.partition(':')
				if part[1]!=':':
					print 'problem partitioning',line
				blindString=part[2]
				bwords=blindString.split()
				if not bwords[-1].isdigit():
					print 'problem parsing blinds'

				if 'small blind' in blindString:
						SB=float(bwords[-1])	
						POT+=SB
				elif 'big blind' in blindString:
						BB=float(bwords[-1])
						POT+=BB
				else:
					print 'problem parsing small blind'
		#		
		#
		#
		#process the ANTE
		if handState=='A':
			if 'posts the ante' in line:
				anteamount=line.split()[-1]
				if not anteamount.isdigit():
					print 'problem parsing the ante'
				else:	
					anteSum+=float(line.split()[-1])
				#
			#
			if (not 'posts the ante' in line) and ('posts the ante' in oldLine):
				#done with ante
				Ante=anteSum
				POT+=Ante
		#save in dictionary
		if handState=='A' and (Ante!=None or BB != None):
			#done with the ante and blinds
			if not 'SB' in pokerTableDict: #so that it's only done once
				pokerTableDict['SB']=SB
				pokerTableDict['BB']=BB
				pokerTableDict['Ante']=Ante
		#done with blinds
		#
		#
		#
		#
		#
		#
		#
		#
		#
		#
		#
		#====================================
		#PROCESS ACTIONS
		#====================================
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
					actionDict=parseAction(line)
					if actionDict:
						validAction=True
					else:
						validAction=False
					#
					#get the contribution to the pot from the action:
					if validAction and actionDict['action'] in 'BRC': #bet,raise o check
						amount=actionDict['amount']
						assert amount!=None
						POT+=amount
					else:
						pass
					#
					#
					if validAction: #it's not null so it was a valid action
						actionID+=1
						actionDict['actionID']=actionID
						actionDict['actionState']=handState
						actionDict['pot']=POT
						actionDict['handID']=handID
					#
					#
					#

					#
					#
					#
					#parsedDict['actionDict']=copy.deepcopy(actionDict)
					#return actionDict
					if actionDict:
						insertIntoTable('actions',actionDict,connection)
			#
		#
		#================================
		#PROCESS SUMMARY
		#================================		
		if handState=='Y':

			if 'Total pot' in line:
				potwords=line.split()
				totalPot=potwords[2]
				#if totalPot != POT:
				#	print 'the pots are different',totalPot,POT
				if not totalPot.isdigit():
					print 'totaPot is not a digit'
					assert False
				else:
					totalPot=float(totalPot)
			#
			#get the dealer,SB and BB ids

			if 'Seat' in line:

				semicln=line.find(':')
				for position in ['(button)','(small blind)','(big blind)']:
					if position in line:
					
						pos=line.find(position)
						testName=line[semicln+2:pos-1]
						if not testName in playerNameList:
							print 'the name of the player was not correctly parsed',testName
							assert False
						else:
							if position=='(button)':
								DEALER_ID=copy.copy(testName)
								pokerTableDict['DEALER_ID']=DEALER_ID								
							if position=='(small blind)':
								SB_ID=copy.copy(testName)
								pokerTableDict['SB_ID']=SB_ID								
							if position=='(big blind)':
								BB_ID=copy.copy(testName)
								pokerTableDict['BB_ID']=BB_ID								
		#		
		#
		#
		oldLine=line
	#for lines
	#
	#





#
#
#

if __name__=='__main__':
	a=''
	tableName='actions'
	connection=getConnectionToDataBase()
	print 'starting to parse'
	parsePokerHands(tableName,a,connection)
	print 'done parsing'
