#from Assignment_3 import Assignment_3_Andreasson_Edman
import poker
from PyQt5.QtCore import *
#from PyQt5.QtWidgets import *
import numpy as np


'''
Setup
'''


class Player(QObject):

    new_stack = pyqtSignal()
    player_changed = pyqtSignal()
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
        self.currentbet = currentbet
        self.pot = pot
        self.hand = poker.TableModel()


class GameMaster(QObject):
    next_hand = pyqtSignal()
    game_start = pyqtSignal()
    next_round = pyqtSignal()
    game_message = pyqtSignal((str,))
    ended = pyqtSignal((str,))
    change_player = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.starting_player = 0
        self.deck = poker.Deck()
        self.deck.shuffle_deck()
        NUMBEROFPLAYERS = 2  # int(input('Number of players:'))
        STARTINGSTACK = 2000  # float(input('Set starting stack amount:'))
        self.startingbet = 50  # float(input('Set starting bet:'))
        #self.ActivePlayers = NUMBEROFPLAYERS
        playername =[]
        for i in range(NUMBEROFPLAYERS):
            playername.append ('%s' % str(i + 1) ) # input('Player %d name:' % (i+1))
        self.players = []
        self.table = Table(self.startingbet, 0)
        self.activeplayer = 0
        self.first_action = True
        self.round = 1

        for i in range(NUMBEROFPLAYERS):
            player = Player(STARTINGSTACK, playername[i])
            self.players.append(player)
        print(self.players[0].name)
        self.players[self.starting_player].hand.active=1
        for i in range(2 * NUMBEROFPLAYERS):
            card = self.deck.take_top_card()
            if i > NUMBEROFPLAYERS - 1:
                self.players[i - NUMBEROFPLAYERS].hand.give_card(card)
            else:
                self.players[i].hand.give_card(card)
        self.players[self.starting_player].active = 1
        self.players[self.starting_player].player_changed.emit()
        self.players[int(not self.starting_player)].player_changed.emit()
        self.next_hand.connect(self.end_of_hand)
        self.change_player.connect(self.change_active_player)
        self.next_round.connect(self.round_controller)

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
            for player in self.players:
                player.hand.best_poker_hand(self.table.hand.cards)

            if self.players[0].hand.pokerhand < self.players[1].hand.pokerhand:
                self.winner = 1
                self.win()
            elif self.players[0].hand.pokerhand > self.players[1].hand.pokerhand:
                self.winner = 0
                self.win()
            else:
                self.draw()


    def check_or_call(self):
        if self.table.currentbet == 0:
            if self.first_action:
                self.first_action = False
                self.change_player.emit()
            else:
                self.next_round.emit()
        else:
            if not self.first_action:
                amount = self.table.currentbet
                self.players[self.activeplayer].stack = self.players[self.activeplayer].stack - amount + self.players[self.activeplayer].current_bet
                self.table.pot = self.table.pot + amount - self.players[self.activeplayer].current_bet
                self.table.currentbet = amount
                self.players[self.activeplayer].current_bet = amount
                self.players[self.activeplayer].new_stack.emit()
                self.table.new_pot_or_bet.emit()
                self.next_round.emit()

            else:
                amount = self.table.currentbet
                self.players[self.activeplayer].stack = self.players[self.activeplayer].stack - amount + self.players[
                self.activeplayer].current_bet
                self.table.pot = self.table.pot + amount - self.players[self.activeplayer].current_bet
                self.table.currentbet = amount
                self.players[self.activeplayer].current_bet = amount
                self.players[self.activeplayer].new_stack.emit()
                self.table.new_pot_or_bet.emit()
                self.first_action = False
                self.change_player.emit()

    def compute_bet_limit(self):
        if self.players[self.activeplayer].stack == 0:
            self.game_message.emit('Unable to place bet: You have no money')
            return 0, 0


        elif self.players[int(not self.activeplayer)].stack == 0:
            self.game_message.emit('Unable to place bet: Opponent has no money')
            return 0, 0

        else:
            self.bet_ok = True
            limits = [self.players[self.activeplayer].stack + self.players[self.activeplayer].current_bet,
                      self.players[int(not self.activeplayer)].stack + self.players[
                          int(not self.activeplayer)].current_bet]
            return self.table.currentbet + 1, min(limits)

    def bet(self, amount):

        self.players[self.activeplayer].stack = self.players[self.activeplayer].stack - amount + self.players[self.activeplayer].current_bet
        self.table.pot = self.table.pot + amount - self.players[self.activeplayer].current_bet
        self.table.currentbet = amount
        self.players[self.activeplayer].current_bet = amount
        self.first_action = False
        self.players[self.activeplayer].new_stack.emit()
        self.table.new_pot_or_bet.emit()
        self.change_player.emit()

    def win(self):
        self.players[self.winner].stack = self.players[self.winner].stack + self.table.pot
        self.game_message.emit('Congratulations, player %s won %d $' % (self.players[self.winner].name, self.table.pot))
        self.players[self.winner].new_stack.emit()
        self.next_hand.emit()

    def draw(self):
        self.players[0].stack = self.players[0].stack + self.table.pot / 2
        self.players[1].stack = self.players[1].stack + self.table.pot / 2
        self.players[0].new_stack.emit()
        self.players[1].new_stack.emit()
        self.game_message.emit('Draw, no player won')
        self.next_hand.emit()

    def fold(self):

        self.players[not int(self.activeplayer)].stack = self.players[not int(self.activeplayer)].stack + self.table.pot
        self.players[not int(self.activeplayer)].new_stack.emit()
        self.game_message.emit('Congratulations, player %s won %d $' %( self.players[not int(self.activeplayer)].name, self.table.pot))
        self.table.new_pot_or_bet.emit()
        self.next_hand.emit()

    def flop(self):
        self.table.currentbet = 0
        self.table.new_pot_or_bet.emit()
        for i in range(0, 3):
            card = self.deck.take_top_card()
            self.table.hand.give_card(card)

    def river(self):
        self.table.currentbet = 0
        card = self.deck.take_top_card()
        self.table.hand.give_card(card)
        self.table.new_pot_or_bet.emit()

    def end_of_hand(self):
        if self.players[0].stack == 0:
            self.ended.emit('Congratulations, player 2 won the game')

        elif self.players[1].stack == 0:
            self.ended.emit('Congratulations, player 1 won the game')
        else:
            self.table.pot = 0
            self.deck = poker.Deck()
            self.deck.shuffle_deck()
            self.players[0].hand.remove_card(np.s_[:])
            self.players[1].hand.remove_card(np.s_[:])
            self.table.hand.remove_card(np.s_[:])
            self.new_hand()

    def change_active_player(self):
        self.players[self.activeplayer].hand.flipped_cards = True
        self.players[self.activeplayer].hand.data_changed.emit()
        self.activeplayer = int(not self.activeplayer)
        self.players[0].hand.active = not self.players[0].hand.active
        self.players[1].hand.active = not self.players[1].hand.active
        self.players[int (not self.activeplayer)].player_changed.emit()
        self.players[self.activeplayer].player_changed.emit()

    def new_hand(self):
        self.players[self.activeplayer].hand.flipped_cards = True
        self.players[self.activeplayer].hand.data_changed.emit()
        self.starting_player =int(not self.starting_player)
        if not (self.activeplayer == self.starting_player):
            self.change_player.emit()
        self.table.currentbet = min(self.startingbet, self.players[0].stack, self.players[1].stack)
        self.round = 0
        self.table.new_pot_or_bet.emit()
        for i in range(0, 2):
            card = self.deck.take_top_card()
            self.players[0].hand.give_card(card)
            card = self.deck.take_top_card()
            self.players[1].hand.give_card(card)
        self.next_round.emit()


