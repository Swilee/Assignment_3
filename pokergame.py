from Assignment_3 import Assignment_3_Andreasson_Edman
from Assignment_3 import poker, card_view
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *

import sys
'''
Setup
'''

pot = 0
NumberOfPlayers = 2#int(input('Number of players:'))
Playername=[None]*NumberOfPlayers
for i in range(0, NumberOfPlayers):
    Playername[i] = '%s' % str(i+1)  #input('Player %d name:' % (i+1))

STARTINGSTACK = 2000  # float(input('Set starting stack amount:'))
STARTINGBET = 50   # float(input('Set starting bet:'))
ActivePlayers = NumberOfPlayers
Players = []


class Player(QObject):
    new_stack = pyqtSignal()

    def __init__(self, startingstack, playername, button):
        super().__init__()
        self.stack = startingstack
        self.name = playername
        self.hand = poker.Playerhandmodel()
        button.check_press.connect(self.remove_player)
        button.fold_press.connect(self.fold)

    def bet(self, amount):
        self.stack = self.stack - amount
        self.new_stack.emit()

    def win(self, pot):
        self.stack = self.stack + pot
        self.new_stack.emit()

    def fold(self):
        print('du har foldat')
        self.hand.cards = []
        self.active = 0


    def remove_player(self):
        print('button got pressed')


class Table(QObject):
    def __init__(self, currentbet, pot):
        super().__init__()
        self.CurrentBet = currentbet
        self.Pot = pot
        self.hand = poker.TableModel()


btn = Assignment_3_Andreasson_Edman.Buttons()

for i in range(0, NumberOfPlayers):
    player = Player(STARTINGSTACK, Playername[i], btn)
    Players.append(player)


class Gamemaster:
    def __init__(self):
        self.starting_player = 0
        self.deck=poker.Deck()
        self.deck.ShuffleDeck()
        self.players = Player

        fold.connect(self.end_of_round)

    def flop(self,table):
        for i in range(3):
            card = self.deck.TakeTopCard()
            table.hand.givecard(card)
        return table

    def river(self, table):
        

    def end_of_round(self, players):
        if players[0].stack == 0:
            print('Player 2 wins')
            sys.exit()
        elif players[1].stack==0:
            print('player 1 wins')
            sys.exit()
        else:
            self.starting_player = int(not self.starting_player)
            self.deck = poker.Deck()
            self.deck.ShuffleDeck()
            players[0].hand.removecard(:)
            players[1].hand.removecard(:)
            return players


    def change_active_player(self):
            self.activeplayer = int(not self.activeplayer)


    def New_Round(self, players):
        self.activeplayer = self.starting_player
        for i in range(0, 2):
            card = self.deck.TakeTopCard()
            players[0].hand.givecard(card)
            card = self.deck.TakeTopCard()
            players[1].hand.givecard(card)
        return players


#starta
CurrentBet = STARTINGBET
Deck = poker.Deck()
Deck.ShuffleDeck()
for i in range(0, 2*NumberOfPlayers):
    card = Deck.TakeTopCard()
    if i > NumberOfPlayers-1:
        Players[i-NumberOfPlayers].hand.givecard(card)
    else:
        Players[i].hand.givecard(card)

app = Assignment_3_Andreasson_Edman.QApplication(sys.argv)

table = Table(CurrentBet, pot)
print(int(not 1))
print(int(not 0))

tablebox = Assignment_3_Andreasson_Edman.Tablewindow(table)
player1box = Assignment_3_Andreasson_Edman.Playerwindow(Players[0])

player2box = Assignment_3_Andreasson_Edman.Playerwindow(Players[1])
game = Assignment_3_Andreasson_Edman.PokerWindow()

game.Create_GUI(player1box, player2box, tablebox, btn)

game.show()

for i in range(5):
    card = Deck.TakeTopCard()
    table.hand.givecard(card)

app.exec_()

#game = Assignment_3_Andreasson_Edman.PokerWindow()
#game.show()