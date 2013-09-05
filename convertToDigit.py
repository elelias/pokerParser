# coding: utf-8
import sys,os
from isNumber import *

def convertToDigit(word,thisHand,warn=True):
	'''takes an input like $bblabla and returns the digit'''

	#sanity check
	if (thisHand.gameType!='T'): #the first character should be the currency symbol
		if word[0]!= thisHand.currencySymbol:
			print 'the first character is not the currency symbol'
			print 'the word is='+word
			print 'the currencySymbol should be',thisHand.currencySymbol
		else:
			word=word[1:]	

	if not isNumber(word):
		#print 'the conversion did not work'
		#print 'the word is now'+word
		#print 'which is of type',type(word)
		return None

	else:
		return float(word)
	#
#