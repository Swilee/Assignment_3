from Assignment_3 import Assignment_3_Andreasson_Edman
from Assignment_3 import poker, card_view
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
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


    def remove_player(self):
        print('button got pressed')


class Table(QObject):
    new_pot_or_bet = pyqtSignal()
    def __init__(self, currentbet, pot):
        super().__init__()
        self.CurrentBet = currentbet
        self.Pot = pot
        self.hand = poker.TableModel()

class Gamemaster(QObject):
    next_hand = pyqtSignal()
    game_start = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.starting_player = 0
        self.deck = poker.Deck()
        self.deck.ShuffleDeck()
        self.players = Player
        self.NumberOfPlayers = 2  # int(input('Number of players:'))
        self.Playername = [None] * self.NumberOfPlayers
        for i in range(0, self.NumberOfPlayers):
            self.Playername[i] = '%s' % str(i + 1)  # input('Player %d name:' % (i+1))

        self.STARTINGSTACK = 2000  # float(input('Set starting stack amount:'))
        self.STARTINGBET = 50  # float(input('Set starting bet:'))
        self.ActivePlayers = self.NumberOfPlayers
        self.Players = []
        self.table = Table(self.STARTINGBET, 0)
        self.btn = Assignment_3_Andreasson_Edman.Buttons()
        self.activeplayer=0

        for i in range(0, self.NumberOfPlayers):
            player = Player(self.STARTINGSTACK, self.Playername[i])
            self.Players.append(player)


        for i in range(0, 2 * self.NumberOfPlayers):
            card = self.deck.TakeTopCard()
            if i > self.NumberOfPlayers - 1:
                self.Players[i - self.NumberOfPlayers].hand.givecard(card)
            else:
                self.Players[i].hand.givecard(card)
        self.btn.betbutton.clicked.connect(self.bet)
        self.btn.foldbutton.clicked.connect(self.fold)
        self.next_hand.connect(self.end_of_hand)
        self.game_start.connect(self.river)


    def bet(self):
        if self.Players[self.activeplayer].stack>self.table.CurrentBet:
             amount, ok = QInputDialog.getInt(QInputDialog(), 'Bet', 'Enter bet (min = %d, max = %d)' % (
             self.table.CurrentBet, self.Players[self.activeplayer].stack), min=self.table.CurrentBet,
                                         max=self.Players[self.activeplayer].stack)
             amount = int(amount)
        else:
            amount = self.Players[self.activeplayer].stack
            ok = True
        if ok:
            self.Players[self.activeplayer].stack = self.Players[self.activeplayer].stack - amount
            self.table.Pot = self.table.Pot+amount
            self.table.CurrentBet = amount
            self.Players[self.activeplayer].new_stack.emit()
            self.table.new_pot_or_bet.emit()
            self.activeplayer = int(not self.activeplayer)



    def win(self):
        self.Players[self.winner].stack = self.Players[self.winner].stack + self.table.Pot
        self.Players[self.winner].new_stack.emit()

    def fold(self):
        self.Players[not int(self.activeplayer)].stack = self.Players[not int(self.activeplayer)].stack + self.table.Pot
        self.Players[not int(self.activeplayer)].new_stack.emit()
        ans = QMessageBox.information(QMessageBox(), 'Player won',
                                   'Congratulations, %s won' % self.Players[not int(self.activeplayer)].name, QMessageBox.Ok)
        self.next_hand.emit()


    def start(self):
        self.app = Assignment_3_Andreasson_Edman.QApplication(sys.argv)
        self.tablebox = Assignment_3_Andreasson_Edman.Tablewindow(self.table)
        self.player1box = Assignment_3_Andreasson_Edman.Playerwindow(self.Players[0])
        self.player2box = Assignment_3_Andreasson_Edman.Playerwindow(self.Players[1])
        self.game = Assignment_3_Andreasson_Edman.PokerWindow()
        self.game.Create_GUI(self.player1box, self.player2box, self.tablebox, self.btn)
        self.game.show()
        self.game_start.emit()
        self.app.exec_()


    def flop(self):
        for i in range(0, 3):
            card = self.deck.TakeTopCard()
            self.table.hand.givecard(card)

    def river(self):
        card = self.deck.TakeTopCard()
        self.table.hand.givecard(card)

    def end_of_hand(self):
        if self.Players[0].stack == 0:
            print('Player 2 wins')
            sys.exit()
        elif self.Players[1].stack == 0:
            print('player 1 wins')
            sys.exit()
        else:
            self.starting_player = int(not self.starting_player)
            self.deck = poker.Deck()
            self.deck.ShuffleDeck()
            self.Players[0].hand.removecard(np.s_[:])
            self.Players[1].hand.removecard(np.s_[:])
            self.table.hand.removecard(np.s_[:])
            self.new_hand()


    def change_active_player(self):
            self.activeplayer = int(not self.activeplayer)


    def new_hand(self):
        self.activeplayer = self.starting_player
        self.table.CurrentBet = self.STARTINGBET
        self.table.pot = 0
        self.table.new_pot_or_bet.emit()
        for i in range(0, 2):
            card = self.deck.TakeTopCard()
            self.Players[0].hand.givecard(card)
            card = self.deck.TakeTopCard()
            self.Players[1].hand.givecard(card)




Gamemaster().start()
