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

		handNumber=line[start+1:end]
		if not handNumber.isdigit():
			print 'this is not a valid number',line
			assert False
		else:
			self.handNumber=handNumber

	def extractCurrency(self,line):
		#get the currency and the quantity:
		lineSplit=line.split()
		self.gameCurrency=None
		for piece in lineSplit:
			if self.gameType=='zoom':
				if piece[:2]=='($':
					self.gameCurrency=='D'
				elif piece[:2]==u'(€':
					self.gameCurrency=='E'
				else:
					self.gameCurrency='U'
				#
			#
			if self.gameType=='tournament':
				if piece[0:1] == '$':
					self.gameCurrency='D'
				elif piece[0:1]==u'€':
					self.gameCurrency='E'
				else:
					self.gameCurrency='U'
				#
			#
			if self.gameCurrency != None:
				break


		assert self.gameType!=None
		assert self.gameCurrency!=None

	def makeCurrencySymbol(self):
		if self.currency=='D':
			self.currencySymbol='$'
		elif self.currency=='E':
			self.currencySymbol=u'€'
		else:
			self.currencySymbol=None

	def initializeWithLine(self,line):
		'''initialize'''def parseHandInfo(line):

		'''parses the type of game from line'''

		if 'Zoom' in line:
			self.gameType='Z'
		elif 'Tournament' in line:
			self.gameType='T'
		else:
			self.gameType='unknown'
		#

		extractHandIDFromLine(line)
		extractCurrency(line)
		makeCurrencySymbol()


	def setNPlayers(self,n):
		self.nPlayers=n
	#

	def convertToDict(inputDict={}):
		'''converts the hand to a dictionary'''
		outDict=copy.deepcopy(inputDict)
		outDict['currency']=self.currency
		outDict['gameType']=self.gameType
		outDict['handID']=self.handNumber
		outDict['SB']=self.SB
		outDict['BB']=self.BB
		outDict['Ante']=self.Ante
		outDict['SB_ID']=self.SB_ID
		outDict['BB_ID']=self.BB_ID
		outDict['DEALER_ID']=self.DEALER_ID
		return outDict


	def __init__(self,line):
		currency=None
		nPlayers=0
		self.gameType=None
		currencySymbol=None
		handNumber=None
		SB=None
		BB=None
		Ante=None
		SB_ID=None
		BB_ID=None
		DEALER_ID=None
		initializeWithLine(line)




