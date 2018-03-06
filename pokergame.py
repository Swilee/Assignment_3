from Assignment_3 import Assignment_3_Andreasson_Edman
from Assignment_3 import poker, card_view
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
import time

import sys
'''
Setup
'''



class Player(QObject):
    new_stack = pyqtSignal()
    def __init__(self, startingstack, playername):
        super().__init__()
        self.stack = startingstack
        self.name = playername
        self.hand = poker.Playerhandmodel()
        #button.check_press.connect(self.remove_player)
        #button.fold_press.connect(self.fold)

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





class Gamemaster(QObject):

    game_start = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.starting_player = 0
        self.deck = poker.Deck()
        self.deck.ShuffleDeck()
        self.players = Player
        self.pot = 0
        self.NumberOfPlayers = 2  # int(input('Number of players:'))
        self.Playername = [None] * self.NumberOfPlayers
        for i in range(0, self.NumberOfPlayers):
            self.Playername[i] = '%s' % str(i + 1)  # input('Player %d name:' % (i+1))

        self.STARTINGSTACK = 2000  # float(input('Set starting stack amount:'))
        self.STARTINGBET = 50  # float(input('Set starting bet:'))
        self.ActivePlayers = self.NumberOfPlayers
        self.Players = []
        self.CurrentBet = self.STARTINGBET
        self.table = Table(self.CurrentBet, self.pot)
        self.btn = Assignment_3_Andreasson_Edman.Buttons()


        for i in range(0, self.NumberOfPlayers):
            player = Player(self.STARTINGSTACK, self.Playername[i])
            self.Players.append(player)


        for i in range(0, 2 * self.NumberOfPlayers):
            card = self.deck.TakeTopCard()
            if i > self.NumberOfPlayers - 1:
                self.Players[i - self.NumberOfPlayers].hand.givecard(card)
            else:
                self.Players[i].hand.givecard(card)



        #fold.connect(self.end_of_round)

    def start(self):
        self.app = Assignment_3_Andreasson_Edman.QApplication(sys.argv)
        self.tablebox = Assignment_3_Andreasson_Edman.Tablewindow(self.table)
        self.player1box = Assignment_3_Andreasson_Edman.Playerwindow(self.Players[0])
        self.player2box = Assignment_3_Andreasson_Edman.Playerwindow(self.Players[1])
        self.game = Assignment_3_Andreasson_Edman.PokerWindow()
        self.game.Create_GUI(self.player1box, self.player2box, self.tablebox, self.btn)
        self.game.show()
        self.app.exec_()

    def flop(self,table):
        for i in range(3):
            card = self.deck.TakeTopCard()
            table.hand.givecard(card)
        return table

    def river(self, table):
        a

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
            self.Players[0].hand.removecard(all)
            self.Players[1].hand.removecard(all)
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
Gamemaster().start()

#game = Assignment_3_Andreasson_Edman.PokerWindow()
#game.show()