
import sys,os
from convertToDigit import *

def extractPlayerInfoFromLine(line,thisHand):
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
	#
	#
	#process the stack of the player:
	playerStackLine=line[parenth+1:]
	playerStackWords=playerStackLine.split()


	stackWord=playerStackWords[0]
	playerStack=convertToDigit(stackWord,thisHand)

	if  playerStackWords[2]!='chips)':
		print 'the line does not contain chips in it'
		print 'the line is='+playerStackLine
		assert False

	return {'playerNumber':playerNumber,'playerName':playerName,'playerStack':playerStack}




