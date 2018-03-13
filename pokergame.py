#from Assignment_3 import Assignment_3_Andreasson_Edman
from Assignment_3 import poker
from PyQt5.QtCore import *
#from PyQt5.QtWidgets import *
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
    game_message = pyqtSignal((str,))

    def __init__(self):
        super().__init__()
        self.starting_player = 0
        self.deck = poker.Deck()
        self.deck.shuffle_deck()
        self.NumberOfPlayers = 2  # int(input('Number of players:'))
        self.STARTINGSTACK = 2000  # float(input('Set starting stack amount:'))
        self.STARTINGBET = 50  # float(input('Set starting bet:'))
        self.ActivePlayers = self.NumberOfPlayers
        Playername = [None] * self.NumberOfPlayers

        for i in range(self.NumberOfPlayers):
            Playername[i] = '%s' % str(i + 1)  # input('Player %d name:' % (i+1))

        self.players = []
        self.table = Table(self.STARTINGBET, 0)
        self.activeplayer = 0
        self.first_action = True
        self.round = 0

        for i in range(0, self.NumberOfPlayers):
            player = Player(self.STARTINGSTACK, Playername[i])
            self.players.append(player)
        self.players[self.starting_player].hand.active=1
        for i in range(0, 2 * self.NumberOfPlayers):
            card = self.deck.take_top_card()
            if i > self.NumberOfPlayers - 1:
                self.players[i - self.NumberOfPlayers].hand.give_card(card)
            else:
                self.players[i].hand.give_card(card)

        self.app = Assignment_3_Andreasson_Edman.QApplication(sys.argv)
        self.tablebox = Assignment_3_Andreasson_Edman.TableWindow(self.table)
        self.players[0].playerbox = Assignment_3_Andreasson_Edman.PlayerWindow(self.players[0])
        self.players[1].playerbox = Assignment_3_Andreasson_Edman.PlayerWindow(self.players[1])
        self.players[self.starting_player].playerbox.set_to_active()
        self.players[int(not self.starting_player)].playerbox.set_to_inactive()

        self.btn = Assignment_3_Andreasson_Edman.Buttons()
        self.btn.betbutton.clicked.connect(self.bet)
        self.btn.foldbutton.clicked.connect(self.fold)
        self.btn.checkbutton.clicked.connect(self.check_or_call)

        self.next_hand.connect(self.end_of_hand)
        self.game_start.connect(self.round_controller)
        self.change_player.connect(self.change_active_player)
        self.next_round.connect(self.round_controller)

        self.game = Assignment_3_Andreasson_Edman.PokerWindow(self.players[0].playerbox, self.players[1].playerbox, self.tablebox, self.btn)
        self.game.show()
        self.game_start.emit()
        self.app.exec_()

    def round_controller(self):
        self.players[0].current_bet = 0
        self.players[1].current_bet = 0
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
            best_hands = [player.best_poker_hand(self.table.hand.cards) for player in self.players]

            if best_hands[0] < best_hands[1]:
                self.winner = 1
                self.win()
            elif best_hands[0] > best_hands[1]:
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
                self.players[self.activeplayer].stack = self.players[self.activeplayer].stack - amount + self.players[self.activeplayer].current_bet
                self.table.Pot = self.table.Pot+amount - self.players[self.activeplayer].current_bet
                self.table.CurrentBet = amount
                self.players[self.activeplayer].new_stack.emit()
                self.table.new_pot_or_bet.emit()
                self.next_round.emit()
            else:
                amount = self.table.CurrentBet
                self.players[self.activeplayer].stack = self.players[self.activeplayer].stack - amount + self.players[
                self.activeplayer].current_bet
                self.table.Pot = self.table.Pot + amount - self.players[self.activeplayer].current_bet
                self.table.CurrentBet = amount
                self.players[self.activeplayer].new_stack.emit()
                self.table.new_pot_or_bet.emit()
                self.first_action = False
                self.change_player.emit()

    def compute_bet_limit(self):
        limits = [self.players[self.activeplayer].stack + self.players[self.activeplayer].current_bet,
                  self.players[int(not self.activeplayer)].stack + self.players[
                      int(not self.activeplayer)].current_bet]
        return self.table.CurrentBet+1, min(limits)

    def bet(self, amount):
        if self.players[self.activeplayer].stack == 0:
            QMessageBox.information(QMessageBox(), 'Betting error',
                                    'Unable to place bet: You have no money')

        elif self.players[int(not self.activeplayer)].stack == 0:
            QMessageBox.information(QMessageBox(), 'Betting error',
                                    'Unable to place bet: Opponent has no money')

        else:
            if self.players[self.activeplayer].stack+self.players[self.activeplayer].current_bet > self.table.CurrentBet:
                min_bet, max_bet = self.compute_bet_limit()
                amount, ok = QInputDialog.getInt(QInputDialog(), 'Bet', 'Enter bet (min = %d, max = %d)' % (
                    min_bet, max_bet, min=min_bet, max=max_bet)

                amount = int(amount)
            else:
                amount = self.Players[self.activeplayer].stack + self.Players[self.activeplayer].current_bet
                ok = True
            if ok:
                self.players[self.activeplayer].stack = self.Players[self.activeplayer].stack - amount + self.Players[self.activeplayer].current_bet
                self.table.Pot = self.table.Pot + amount - self.Players[self.activeplayer].current_bet
                self.table.CurrentBet = amount
                self.players[self.activeplayer].current_bet = amount
                self.first_action = False
                self.players[self.activeplayer].new_stack.emit()
                self.table.new_pot_or_bet.emit()
                self.change_player.emit()

    def win(self):
        self.players[self.winner].stack = self.players[self.winner].stack + self.table.Pot
        QMessageBox.information(QMessageBox(), 'Player won',
                                   'Congratulations, player %s won %d $' % (self.players[self.winner].name, self.table.Pot), QMessageBox.Ok)
        self.players[self.winner].new_stack.emit()
        self.next_hand.emit()

    def draw(self):
        self.players[0].stack = self.players[0].stack + self.table.Pot / 2
        self.players[1].stack = self.players[1].stack + self.table.Pot / 2
        self.players[0].new_stack.emit()
        self.players[1].new_stack.emit()
        QMessageBox.information(QMessageBox(),
                                   'Draw', 'No Player won')
        self.next_hand.emit()

    def fold(self):

        self.players[not int(self.activeplayer)].stack = self.players[not int(self.activeplayer)].stack + self.table.Pot
        self.players[not int(self.activeplayer)].new_stack.emit()
        #self.game_message.emit('Congratulations, player %s won ' % self.Players[not int(self.activeplayer)].name)
        QMessageBox.information(QMessageBox(), 'Player won',
                                   'Congratulations, player %s won ' % self.players[not int(self.activeplayer)].name)

        self.table.new_pot_or_bet.emit()
        self.next_hand.emit()

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
        if self.players[0].stack == 0:
            #self.ended.emit()
            QMessageBox.information(QMessageBox(), 'Game ended',
                                    'Congratulations, player 2 won the game', QMessageBox.Close)
            sys.exit()
        elif self.players[1].stack == 0:
            QMessageBox.information(QMessageBox(), 'Game ended',
                                    'Congratulations, player 2 won the game', QMessageBox.Close)
            sys.exit()
        else:
            self.table.Pot = 0
            self.deck = poker.Deck()
            self.deck.shuffle_deck()
            self.players[0].hand.remove_card(np.s_[:])
            self.players[1].hand.remove_card(np.s_[:])
            self.table.hand.remove_card(np.s_[:])
            self.new_hand()

    def change_active_player(self):
        self.players[self.activeplayer].hand.flipped_cards = True
        self.players[self.activeplayer].hand.data_changed.emit()
        self.players[self.activeplayer].playerbox.set_to_inactive()
        self.activeplayer = int(not self.activeplayer)
        self.players[self.activeplayer].playerbox.set_to_active()
        self.players[0].hand.active = not self.players[0].hand.active
        self.players[1].hand.active = not self.players[1].hand.active

    def new_hand(self):
        self.players[self.activeplayer].hand.flipped_cards = True
        self.players[self.activeplayer].hand.data_changed.emit()
        self.starting_player =int(not self.starting_player)
        if not (self.activeplayer == self.starting_player):
            self.change_player.emit()
        self.table.CurrentBet = min(self.STARTINGBET, self.players[0].stack, self.players[1].stack)
        self.round = 0
        self.table.new_pot_or_bet.emit()
        for i in range(0, 2):
            card = self.deck.take_top_card()
            self.players[0].hand.give_card(card)
            card = self.deck.take_top_card()
            self.players[1].hand.give_card(card)
        self.next_round.emit()


GameMaster()
