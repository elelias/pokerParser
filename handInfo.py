# coding: utf-8

import sys,os
import copy


class handInfo:

	'''this class contains the information about a poker hand'''



	def extractHandIDFromLine(self,line):
		'''extracts the unique hand number from the input text'''

		start=line.find('#')
		if start==-1:
			print 'this line is wrong ->',line
			assert False
		end=line.find(':')

		handID=line[start+1:end]
		if not handID.isdigit():
			print 'this is not a valid number',line
			assert False
		else:
			self.handID=int(handID)

	def extractCurrency(self,line):
		#get the currency and the quantity:
		lineSplit=line.split()
		self.currency=None
		for piece in lineSplit:
			#print 'analyzing'+piece
			if self.gameType=='Z':
				if piece[:2]=='($':
					self.currency='D'
					#print 'yeeah'
				elif piece[:2]=='(€':
					self.currency='E'
				else:
					self.currency=None
				#
			#
			elif self.gameType=='T':
				if piece[0:1] == '$':
					self.currency='D'
				elif piece[0:1]==u'\\u20ac' or piece[0:1]=='\\xe2\\x82\\xac':
					self.currency='E'
				else:
					self.currency=None
				#
			#
			if self.currency != None:
				break

		if self.currency==None:
			print 'the currency was not parsed. The line is: ',line
			print 'the gameType is',self.gameType
			assert False


	def makeCurrencySymbol(self):
		#print 'maing the currencySymbol with',self.currency
		if self.currency=='D':
			self.currencySymbol='$'
		elif self.currency=='E':
			self.currencySymbol=u'€'
		else:
			self.currencySymbol=None

	def parseGameType(self,line):
		'''parses the type of game from line'''
		if 'Zoom' in line:
			self.gameType='Z'
		elif 'Tournament' in line:
			self.gameType='T'
		else:
			self.gameType='unknown'
		#
		if self.gameType==None:
			print 'the gameType was not parsed. The line is: ',line
			assert False		
	#
	#
	#
	#
	def initializeWithLine(self,line):
		'''initialize'''

		self.parseGameType(line)
		self.extractHandIDFromLine(line)
		self.extractCurrency(line)
		self.makeCurrencySymbol()
	#
	#
	#
	#


	def setNPlayers(self,n):
		self.nPlayers=n
	#

	def convertToDict(self,inputDict={}):
		'''converts the hand to a dictionary'''
		outDict=copy.deepcopy(inputDict)
		outDict['currency']=self.currency
		outDict['gameType']=self.gameType
		outDict['handID']=self.handID
		outDict['SB']=self.SB
		outDict['BB']=self.BB
		outDict['Ante']=self.Ante
		outDict['SB_ID']=self.SB_ID
		outDict['BB_ID']=self.BB_ID
		outDict['DEALER_ID']=self.DEALER_ID
		return outDict


	def __init__(self,line):
		self.currency=None
		self.nPlayers=0
		self.gameType=None
		self.currencySymbol=None
		self.handID=None
		self.SB=None
		self.BB=None
		self.Ante=None
		self.SB_ID=None
		self.BB_ID=None
		self.DEALER_ID=None
		self.initializeWithLine(line)




