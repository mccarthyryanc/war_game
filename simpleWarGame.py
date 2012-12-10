# Simple War player
# Description: This script wll randomly "deal out" a deck of cards to two players
#			and play the card game War as many times as you would like. I was
#			using this to generate as many games as possible to test a few
#			statistical/dynamical system theories about the game. For more info
#			on the game "War" visit: http://www.pagat.com/war/war.html
#			-Deck Structure:
#				Each player has its own set of cards (cs). This is an array of
#				integers ranging from 0 (representing no card) to 2-14 (for
#				the number and face cards). This array always has 52 elements.
#				So, a player has lost once it's set of cards only has zeros
#				in it.
#			-Output to CSV:
#				During each game a CSV file is generated containing an entire
#				record of the game. Every two lines gives the states of Players
#				1 and 2 cards after each Battle or War.
# 
#
# Date: March 2010
#
# Author: Ryan Schilt
#		  ryan.schilt@gmail.com
#
# Copyleft: feel free to share/edit/destory as you please :-)

from random import shuffle
import os, sys, csv, logging

#Some logging stuff to help with debugging.
logging.basicConfig(level=logging.DEBUG, filename='debug.log', format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

#change to the right directory
os.chdir('/home/ryans/Documents/wargame/trials')

#Define "player" datatype
class Player:
	def __init__(self,cardNum,cards):
		#total number of cards in hard, start counting at zero
		self.num = cardNum
		#the cards in hard
		self.cs = cards
##END class Player##

#Define battle function
def battle(p1, p2, warDepth,p1zero,p2zero,zeros):
	
	if warDepth != 0:
		logging.debug('WAR!!!')
	else:
		logging.debug('BATTLE!!!')
	logging.debug('    warDepth =' + str(warDepth))
	
	#check if at a zero, Ex: if p1 has zero, then have to remove zero from p2. 
	if p1.cs[warDepth*4] == 0 :
		p2zero = 1
	elif p2.cs[warDepth*4] == 0:
		p1zero = 1
	
	if p1.cs[warDepth*4] > p2.cs[warDepth*4]:
		logging.debug('    Player1 Wins')
		if warDepth == 0:
			temp1 = p1.cs[0]
			temp2 = p2.cs[0]
			del p1.cs[0]
			del p2.cs[0]
			p1.cs.append(0)
			p2.cs.append(0)
			p1.cs[p1.num] = temp2
			p1.cs[p1.num+1] = temp1
			p1.num += 1
			p2.num -= 1
		else:
			temp1 = p2.cs[0:warDepth*4+1]
			temp2 = p1.cs[0:warDepth*4 + 1]
			del p1.cs[0:warDepth*4+1]
			del p2.cs[0:warDepth*4+1]
			p1.cs.extend(zeros[0:warDepth*4 - 1])
			p2.cs.extend(zeros[0:warDepth*4 + 1])
			p1.cs[p1.num-warDepth*4:p1.num] = temp1
			p1.cs[p1.num+1:p1.num+1+warDepth*4] = temp2
			p1.num += 1 + warDepth*4
			p2.num -= 1 + warDepth*4
		logging.debug('    Player1:' + str(p1.cs))
		logging.debug('    Player2:' + str(p2.cs))
		return [p1,p2,p1zero,p2zero]
	elif p1.cs[warDepth*4] < p2.cs[warDepth*4]:
		logging.debug('    Player2 Wins')
		if warDepth == 0:
			temp1 = p1.cs[0]
			temp2 = p2.cs[0]
			del p2.cs[0]
			del p1.cs[0]
			p2.cs.append(0)
			p1.cs.append(0)
			p2.cs[p2.num] = temp1
			p2.cs[p2.num+1] = temp2
			p2.num += 1
			p1.num -= 1
		else:
			temp1 = p2.cs[0:warDepth*4+1]
			temp2 = p1.cs[0:warDepth*4 + 1]
			del p2.cs[0:warDepth*4+1]
			del p1.cs[0:warDepth*4+1]
			p2.cs.extend(zeros[0:warDepth*4 - 1])
			p1.cs.extend(zeros[0:warDepth*4 + 1])
			p2.cs[p2.num-warDepth*4:p2.num] = temp2
			p2.cs[p2.num+1:p2.num+1+warDepth*4] = temp1
			p2.num += 1 + warDepth*4
			p1.num -= 1 + warDepth*4
		logging.debug('    Player1:' + str(p1.cs))
		logging.debug('    Player2:' + str(p2.cs))
		return [p1,p2,p1zero,p2zero]
	else:
		return battle(p1,p2,warDepth+1,p1zero,p2zero,zeros)
		
##END func battle##

def main():
	#Various Game Variables
	n = 1 			# total number of games
	name = "trial_" 	# basename for datafile
	maxIter = 8000		# max number of Battles/Wars per game
	
	#start iterating through multi-game
	for i in range(n):
		logging.debug('-----------------Begin Game: '+str(i)+' -----------------')
		finname = name + str(i) + ".csv"
		wfile = open(finname, 'wd')
		writer = csv.writer(wfile, delimiter=' ')
	
		#set dealVar to False to use predefined deck.
		dealvar = True
		zeros = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		
		if dealvar:
			#H = hearts, D = diamonds, S = spades, C = clubs
			#11 = jack, 12 = queen, 13 = king, 14 = ace
			deck = [x for y in 'HDSC' for x in range(2,15)]
			
			#define player 1 and 2, remember counting starts at zero
			p1 = Player(25, [])
			p2 = Player(25, [])
			
			#shuffle the deck and pass out to players
			shuffle(deck)
			p1.cs = deck[0::2]
			p2.cs = deck[1::2]
				
			#pad each player with zeros, because a player will have max of 52 cards
			p1.cs.extend(zeros)
			p2.cs.extend(zeros)
		else:
			#define player 1 and 2, remember counting starts at zero
			p1 = Player(25, [])
			p2 = Player(25, [])
			p1.cs = [5, 8, 6, 4, 8, 9, 7, 4, 2, 12, 7, 9, 3, 2, 3, 2, 6, 11, 12, 4, 10, 5, 6, 10, 13, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			p2.cs = [5, 7, 3, 10, 8, 9, 8, 14, 14, 2, 4, 12, 12, 13, 9, 6, 10, 5, 13, 14, 11, 11, 13, 14, 11, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	
		logging.debug('Player 1 Cards:')
		logging.debug(str(p1.cs))
		logging.debug('Player 2 Cards:')
		logging.debug(str(p2.cs))
	
		#intialize counter
		count = 0
	
		#Start game loop
		while ((p1.num + 1 > 0) & (p2.num + 1 > 0)) & (count < maxIter):
			warDepth = 0
			count += 1
			p1zero = 0
			p2zero = 0
			
			[p1,p2,p1zero,p2zero] = battle(p1,p2,warDepth,p1zero,p2zero,zeros)
			
			#quick zero check if game ends on war
			if p1.cs[0] == 0:
				p2.cs = [x for x in p2.cs if x != 0]
			elif p2.cs[0] == 0:
				p1.cs = [x for x in p1.cs if x != 0]
			
			#write data to file
			writer.writerow(p1.cs)
			writer.writerow(p2.cs)
			
			logging.debug('     status:' + ' Iteration =' + str(count))
			logging.debug('        Player1: num =' + str(p1.num) + 'listlength =' + str(len(p1.cs)))
			logging.debug('       ' + str(p1.cs))
			logging.debug('        Player2: num =' + str(p2.num) + 'listlength =' + str(len(p2.cs)))
			logging.debug('       ' + str(p2.cs))
		##END while loop
	
		#check if reached counter and close file
		if count == maxIter:
			writer.writerow([9999])
			wfile.close()
		else:
			wfile.close()
	##END for loop

if __name__ == "__main__":
    main()
