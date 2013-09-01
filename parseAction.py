#
# POKERSTARS ACTION PARSER
#
import sys
import MySQLdb as mdb
import copy


def parseAction(actionLine):
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
		if not actionWords[1].isdigit():
			print 'the second field of the action is not a digit in parseAction'
			print 'the actionName is',actionName
		else:
			actionQuantity=float(actionWords[1])
	#
	#
	#categories:
	#bet
	#raise
	#call
	#fold
	if 'bets' in actionName:
		action='bet'
	elif 'raises' in actionName:
		action='raise'
	elif 'calls' in actionName:
		action='call'
	elif 'folds' in actionName:
		action='fold'
	else:
		print 'action unaccounted for in parseAction'
		print 'the actionName string was',actionName
		action=None

	assert action!=None
	#
	#
	#
	isAllIn=False
	if 'all-in' in actionString:
		isAllIn=True
	#
	#
	actionDict['action']=action
	actionDict['actionQuantity']=actionQuantity
	actionDict['isAllIn']=isAllIn
	actionDict['actingPlayer']=actingPlayer
	return actionDict

if __name__=='__main__':

	actionLine='antimamalos: folds'
	actionDict=parseAction(actionLine)
	#print actionDict
