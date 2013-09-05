#
# coding: utf-8
# POKERSTARS ACTION PARSER
#
import sys
import MySQLdb as mdb
import copy
from isNumber import *
from convertToDigit import *

def parseAction(actionLine,thisHand):
	'''parses the action from a line of input'''

	actionDict={}
	#pokerstars allows for spaces in usernames, so careful when extracting the name
	# the structure is  playerName:action (quantity)
	semicln=actionLine.find(':')
	actingPlayer=actionLine[:semicln]
	#print 'the player acting is',actingPlayer
	actionString=actionLine[semicln+2:] #+2 to remove the extra space after the semicolon
	actionWords=actionString.split()
	
	#the action field can't be empty
	assert(len(actionWords)>0)

	actionQuantity=None
	actionName=actionWords[0]
	if len(actionWords)>1:

		if not actionWords[0] in ['shows','doesn\'t','mucks','folds']:
			actionQuantity=convertToDigit(actionWords[1],thisHand)			
			if actionQuantity==None:
				print 'the actionQuantity conversion did not work'
				print 'actionWords[1] ',actionWords[1]
				print 'the actionLine is ',actionLine
				assert False
	#
	#categories:
	#bet
	#raise
	#call
	#fold
	if 'bets' in actionName:
		action='B'
	elif 'raises' in actionName:
		action='R'
	elif 'calls' in actionName:
		action='C'
	elif 'checks' in actionName:
		action='X'		
	elif 'mucks' in actionName:
		action='M'				
	elif 'folds' in actionName:
		action='F'
	elif 'shows' in actionName or 'doesn\'t' in actionName:
		action='S'
	else:
		print 'action unaccounted for in parseAction'
		print 'the actionName string was',actionName
		action=None


	assert action!=None
	#
	#
	#
	#	
	raiseSize=None
	if action=='R':
		#the structure is 'raises X to Y'
		#with X the size of the raise
		#and  Y the total size of the bet
		assert actionWords[0]=='raises'
		assert actionWords[2]=='to'
		raiseSize=convertToDigit(actionWords[1],thisHand)
		actionQuantity=convertToDigit(actionWords[3],thisHand)
	#
	#
	#
	isAllIn=False
	if 'all-in' in actionString:
		isAllIn=True
	#
	#
	actionDict['action']=action
	actionDict['amount']=actionQuantity
	actionDict['isAllIn']=isAllIn
	actionDict['actingPlayer']=actingPlayer
	actionDict['raiseSize']=raiseSize
	return actionDict

if __name__=='__main__':

	actionLine='antimamalos: folds'
	actionDict=parseAction(actionLine)
	#print actionDict
