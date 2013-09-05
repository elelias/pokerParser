#
# coding: utf-8
# POKERSTARS HISTORY PARSER
#
import sys
import MySQLdb as mdb
import copy
import codecs
from handInfo import *
from parseAction import *
from insertIntoDB import *
from convertToDigit import *
from isNumber import *
from playerInfo import *
from getConnectionToDB import *


#===================================================
#  PARSE THE POKERHANDS
#===================================================
def parsePokerHands(fileName,connection):

	#from handInfo import *
	'''parses the info inside of a file and stores it into the database'''

	inFile=codecs.open(fileName,'r','utf-8')

	handInfoDict={}
	oldLine=''
	#
	#
	#
	for line in inFile:
		#
		#
		#
		if 'PokerStars' in line and 'Hand #' in line:
			newHand=True
		else:
			newHand=False

		if line in ['\n', '\r\n'] and (oldLine not in ['\n', '\r\n'] ):
			lastLine=True
		else:
			lastLine=False

		#initialize stuff:
		if newHand:
			#
			#
			#send the previous record into the DB
			#verbose=True;
			if handInfoDict:
				insertIntoTable('pokerHand',handInfoDict,connection)
			#
			actionID=0
			actionDict={}
			anteSum=0.0
			POT=0.0
			gameType=None
			thisHand=handInfo(line) #initializes the instance of handInfo

		#			
		#
		#
		if lastLine:
			handInfoDict=thisHand.convertToDict()
		#
		#
		#
		#
		#edetermine the hand state (setup/preflop/flop/turn/river/showdown)
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
		try:
			handState=='A'
		except UnboundLocalError:
			print 'fuck! the handState is not set, the line is ',line
		#
		#
		#initialize shit on a new Hand
		if newHand:
			activePlayers=[]
			playerNameList=[]
		#
		#
		#
		#
		#obtain the name of the players and their info before the round
		if handState=='A':
			if  line[0:4]=='Seat':				
				playerInfo=extractPlayerInfoFromLine(line,thisHand)
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
				whereblind=bwords.index('blind')
				blindAmount=convertToDigit(bwords[whereblind+1],thisHand)
				if not isNumber(blindAmount):
					print 'problem parsing blinds'
					print 'this happened on the line',line

				if 'small blind' in blindString:
						thisHand.SB=float(blindAmount)
						POT+=thisHand.SB
				elif 'big blind' in blindString:
						thisHand.BB=float(blindAmount)
						POT+=thisHand.BB
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
				thisHand.Ante=anteSum
				POT+=thisHand.Ante

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
					actionDict=parseAction(line,thisHand)
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
						actionDict['handID']=thisHand.handID
					#
					#
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
				totalPot=convertToDigit(totalPot,thisHand)
				if totalPot==None:
					print 'the converstion of totalPot didnt work ',potwords[2]
			#
			#get the dealer,SB and BB ids

			if 'Seat' in line:

				semicln=line.find(':')
				for position in ['(button)','(small blind)','(big blind)']:
					if position in line:
					
						pos=line.find('(')
						testName=line[semicln+2:pos-1]
						if not testName in playerNameList:
							print 'the name of the player was not correctly parsed',testName
							print 'the list of the players is',playerNameList
							print 'and this happened in line',line
							assert False
						else:
							if position=='(button)':
								thisHand.DEALER_ID=copy.copy(testName)
							if position=='(small blind)':
								thisHand.SB_ID=copy.copy(testName)
							if position=='(big blind)':
								thisHand.BB_ID=copy.copy(testName)
							
		#		
		#
		#
		oldLine=line
	#for lines
	#
	#



def parsePokerHandsFromFiles(fileList,connection):
	'''loops over the files and calls the pokerparser for every file'''

	for file in fileList:
		parsePokerHands(file,connection)

#
#
#

def getListOfFilesFromDir(dirPath):
	import commands as com
	'''gets the list of history files from a certain path'''

	list=com.getoutput('ls '+dirPath).split('\n')
	for a in list:
		if a[0]=='#':
			list.remove(a)
		elif a[-4:]!='.txt':
			list.remove(a)
	return list


def sanitizePath(dirtyPath):
	'''takes care of the spaces inside a path, which ruin everything'''

	
	cleanPath=dirtyPath.replace(' ','\\ ')
	cleanPath=cleanPath.replace('\'','\\\'')
	cleanPath=cleanPath.replace('$','\\$')

	print 'the cleanPath is now',cleanPath
	return cleanPath

	words=dirtyPath.split()
	#print 'the words look like: ',words
	#write a backslash at the end of every word


	for idx,piece in enumerate(words):
		words[idx]+='\\'
	#
	#remove the last backslash
	words[-1]=words[-1][:-1]
	#
	#glue them
	cleanPath=''
	for piece in words:
		cleanPath+=piece+' '
	#


	print 'the cleanPath is',cleanPath
	return cleanPath





#=====================================
# MAIN
#=====================================
if __name__=='__main__':
	a=''
	connection=getConnectionToDataBase()
	print 'starting to parse'

	dirPath='/Users/eliasron/Library/Application Support/PokerStarsEU/HandHistory/elelias01'
	listOfFiles=getListOfFilesFromDir(sanitizePath(dirPath))

	#print listOfFiles
	for file in listOfFiles:
		#print 'dirPath is',dirPath
		print 'parsing the file ',file
		#print 'so  ',dirPath+'/'+file
		parsePokerHands(dirPath+'/'+file,connection)
	#
	print 'done parsing'
