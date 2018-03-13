from Assignment_3 import Assignment_3_Andreasson_Edman
from Assignment_3 import poker
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np

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
        self.hand = poker.PlayerHandModel()
        self.current_bet = 0


class Table(QObject):
    new_pot_or_bet = pyqtSignal()

    def __init__(self, currentbet, pot):
        super().__init__()
        self.CurrentBet = currentbet
        self.Pot = pot
        self.hand = poker.TableModel()


class GameMaster(QObject):
    next_hand = pyqtSignal()
    game_start = pyqtSignal()
    change_player = pyqtSignal()
    next_round = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.starting_player = 0
        self.deck = poker.Deck()
        self.deck.shuffle_deck()
        self.players = Player
        self.NumberOfPlayers = 2  # int(input('Number of players:'))
        self.STARTINGSTACK = 2000  # float(input('Set starting stack amount:'))
        self.STARTINGBET = 50  # float(input('Set starting bet:'))
        self.ActivePlayers = self.NumberOfPlayers
        self.Playername = [None] * self.NumberOfPlayers

        for i in range(0, self.NumberOfPlayers):
            self.Playername[i] = '%s' % str(i + 1)  # input('Player %d name:' % (i+1))

        self.Players = []
        self.table = Table(self.STARTINGBET, 0)
        self.activeplayer = 0
        self.first_action = True
        self.round = 0

        for i in range(0, self.NumberOfPlayers):
            player = Player(self.STARTINGSTACK, self.Playername[i])
            self.Players.append(player)
        self.Players[self.starting_player].hand.active=1
        for i in range(0, 2 * self.NumberOfPlayers):
            card = self.deck.take_top_card()
            if i > self.NumberOfPlayers - 1:
                self.Players[i - self.NumberOfPlayers].hand.give_card(card)
            else:
                self.Players[i].hand.give_card(card)

        self.btn = Assignment_3_Andreasson_Edman.Buttons()
        self.btn.betbutton.clicked.connect(self.bet)
        self.btn.foldbutton.clicked.connect(self.fold)
        self.btn.checkbutton.clicked.connect(self.check_or_call)

        self.next_hand.connect(self.end_of_hand)
        self.game_start.connect(self.round_controller)
        self.change_player.connect(self.change_active_player)
        self.next_round.connect(self.round_controller)

    def round_controller(self):
        self.Players[0].current_bet = 0
        self.Players[1].current_bet = 0
        self.first_action = True
        if not (self.activeplayer == self.starting_player):
            self.change_player.emit()
        if self.round == 0:
            self.round = self.round + 1
            pass
        elif self.round == 1:
            self.round = self.round + 1
            self.flop()
        elif self.round == 2:
            self.round = self.round + 1
            self.river()
        elif self.round == 3:
            self.round = self.round + 1
            self.river()
        elif self.round == 4:
            self.Players[0].hand.best_poker_hand(self.table.hand.cards)
            self.Players[1].hand.best_poker_hand(self.table.hand.cards)

            if self.Players[0].hand.pokerhand < self.Players[1].hand.pokerhand:
                self.winner = 1
                self.win()
            elif self.Players[0].hand.pokerhand > self.Players[1].hand.pokerhand:
                self.winner = 0
                self.win()
            else:
                self.draw()


    def check_or_call(self):
        if self.table.CurrentBet == 0:
            if self.first_action:
                self.first_action = False
                self.change_player.emit()
            else:
                self.next_round.emit()
        else:
            if not self.first_action:
                amount = self.table.CurrentBet
                self.Players[self.activeplayer].stack = self.Players[self.activeplayer].stack - amount + self.Players[self.activeplayer].current_bet
                self.table.Pot = self.table.Pot+amount - self.Players[self.activeplayer].current_bet
                self.table.CurrentBet = amount
                self.Players[self.activeplayer].new_stack.emit()
                self.table.new_pot_or_bet.emit()
                self.next_round.emit()
            else:
                amount = self.table.CurrentBet
                self.Players[self.activeplayer].stack = self.Players[self.activeplayer].stack - amount + self.Players[
                self.activeplayer].current_bet
                self.table.Pot = self.table.Pot + amount - self.Players[self.activeplayer].current_bet
                self.table.CurrentBet = amount
                self.Players[self.activeplayer].new_stack.emit()
                self.table.new_pot_or_bet.emit()
                self.first_action = False
                self.change_player.emit()

    def bet(self):
        if self.Players[self.activeplayer].stack == 0:
            QMessageBox.information(QMessageBox(), 'Betting error',
                                    'Unable to place bet: You have no money')

        elif self.Players[int(not self.activeplayer)].stack == 0:
            QMessageBox.information(QMessageBox(), 'Betting error',
                                    'Unable to place bet: Opponent has no money')

        else:
            if self.Players[self.activeplayer].stack+self.Players[self.activeplayer].current_bet > self.table.CurrentBet:
                limits = [self.Players[self.activeplayer].stack + self.Players[self.activeplayer].current_bet,
                          self.Players[int(not self.activeplayer)].stack + self.Players[
                              int(not self.activeplayer)].current_bet]
                amount, ok = QInputDialog.getInt(QInputDialog(), 'Bet', 'Enter bet (min = %d, max = %d)' % (
                    self.table.CurrentBet+1, min(limits)), min=self.table.CurrentBet+1, max=min(limits))

                amount = int(amount)
            else:
                amount = self.Players[self.activeplayer].stack + self.Players[self.activeplayer].current_bet
                ok = True
            if ok:
                self.Players[self.activeplayer].stack = self.Players[self.activeplayer].stack - amount + self.Players[self.activeplayer].current_bet
                self.table.Pot = self.table.Pot + amount - self.Players[self.activeplayer].current_bet
                self.table.CurrentBet = amount
                self.Players[self.activeplayer].current_bet = amount
                self.first_action = False
                self.Players[self.activeplayer].new_stack.emit()
                self.table.new_pot_or_bet.emit()
                self.change_player.emit()

    def win(self):
        self.Players[self.winner].stack = self.Players[self.winner].stack + self.table.Pot
        QMessageBox.information(QMessageBox(), 'Player won',
                                   'Congratulations, player %s won %d $' % (self.Players[self.winner].name, self.table.Pot), QMessageBox.Ok)
        self.Players[self.winner].new_stack.emit()
        self.next_hand.emit()

    def draw(self):
        self.Players[0].stack = self.Players[0].stack + self.table.Pot / 2
        self.Players[1].stack = self.Players[1].stack + self.table.Pot / 2
        self.Players[0].new_stack.emit()
        self.Players[1].new_stack.emit()
        QMessageBox.information(QMessageBox(),
                                   'Draw', 'No Player won')
        self.next_hand.emit()

    def fold(self):

        self.Players[not int(self.activeplayer)].stack = self.Players[not int(self.activeplayer)].stack + self.table.Pot
        self.Players[not int(self.activeplayer)].new_stack.emit()
        QMessageBox.information(QMessageBox(), 'Player won',
                                   'Congratulations, player %s won ' % self.Players[not int(self.activeplayer)].name)

        self.table.new_pot_or_bet.emit()
        self.next_hand.emit()

    def start(self):
        self.app = Assignment_3_Andreasson_Edman.QApplication(sys.argv)
        self.tablebox = Assignment_3_Andreasson_Edman.TableWindow(self.table)
        self.Players[0].playerbox = Assignment_3_Andreasson_Edman.PlayerWindow(self.Players[0])
        self.Players[1].playerbox = Assignment_3_Andreasson_Edman.PlayerWindow(self.Players[1])
        self.Players[self.starting_player].playerbox.set_to_active()
        self.Players[int(not self.starting_player)].playerbox.set_to_inactive()
        self.game = Assignment_3_Andreasson_Edman.PokerWindow(self.Players[0].playerbox, self.Players[1].playerbox, self.tablebox, self.btn)
        self.game.show()
        self.game_start.emit()
        self.app.exec_()


    def flop(self):
        self.table.CurrentBet = 0
        self.table.new_pot_or_bet.emit()
        for i in range(0, 3):
            card = self.deck.take_top_card()
            self.table.hand.give_card(card)

    def river(self):
        self.table.CurrentBet = 0
        card = self.deck.take_top_card()
        self.table.hand.give_card(card)
        self.table.new_pot_or_bet.emit()

    def end_of_hand(self):
        if self.Players[0].stack == 0:
            QMessageBox.information(QMessageBox(), 'Game ended',
                                    'Congratulations, player 2 won the game', QMessageBox.Close)
            sys.exit()
        elif self.Players[1].stack == 0:
            QMessageBox.information(QMessageBox(), 'Game ended',
                                    'Congratulations, player 2 won the game', QMessageBox.Close)
            sys.exit()
        else:
            self.table.Pot = 0
            self.deck = poker.Deck()
            self.deck.shuffle_deck()
            self.Players[0].hand.remove_card(np.s_[:])
            self.Players[1].hand.remove_card(np.s_[:])
            self.table.hand.remove_card(np.s_[:])
            self.new_hand()

    def change_active_player(self):
        self.Players[self.activeplayer].hand.flipped_cards = True
        self.Players[self.activeplayer].hand.data_changed.emit()
        self.Players[self.activeplayer].playerbox.set_to_inactive()
        self.activeplayer = int(not self.activeplayer)
        self.Players[self.activeplayer].playerbox.set_to_active()
        self.Players[0].hand.active = not self.Players[0].hand.active
        self.Players[1].hand.active = not self.Players[1].hand.active

    def new_hand(self):
        self.Players[self.activeplayer].hand.flipped_cards = True
        self.Players[self.activeplayer].hand.data_changed.emit()
        self.starting_player =int(not self.starting_player)
        if not (self.activeplayer == self.starting_player):
            self.change_player.emit()
        self.table.CurrentBet = min(self.STARTINGBET, self.Players[0].stack, self.Players[1].stack)
        self.round = 0
        self.table.new_pot_or_bet.emit()
        for i in range(0, 2):
            card = self.deck.take_top_card()
            self.Players[0].hand.give_card(card)
            card = self.deck.take_top_card()
            self.Players[1].hand.give_card(card)
        self.next_round.emit()


GameMaster().start()
