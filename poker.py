import numpy as np
from enum import Enum
from enum import IntEnum
from PyQt5.QtCore import *
from abc import ABC, abstractmethod

class Suit(Enum):
    """
    Here an enum class is created to represent the suits.
    """
    Hearts = 0
    Spades = 2
    Diamonds = 1
    Clubs = 3


class HighCard(IntEnum):

    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13
    ace = 14


class CardCombo(IntEnum):
    """
    Here an enum class is created to represent the different values of pokenhands.
    """
    highcard = 0
    onepair = 1
    twopair = 2
    threeofakind = 3
    straight = 4
    flush = 5
    fullhouse = 6
    fourofakind = 7
    straightflush = 8



class PlayingCard(ABC):
    """
    Here a playingcard class is defined to be comparable.
    """

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    @abstractmethod
    def give_value(self):
        raise NotImplementedError

    def __str__(self):
        return '%s %s' %(self.symbol , self.uni)

    def __init__(self):
        self.Uni = [u'\u2665', u'\u2666', u'\u2660', u'\u2663']


class NumberedCard(PlayingCard):
    """
    In this class the playingcards without a suit are represented.
    """
    def __init__(self, value, suit):
        super().__init__()
        self.value = value
        self.suit = suit
        self.uni = self.Uni[suit.value]
        self.symbol = str(value)

    def give_value(self):
        return self.value

class JackCard(PlayingCard):
    '''
    The JackCard class represents the jack card
    '''
    def __init__(self, suit):
        super().__init__()
        self.suit = suit
        self.value = 11
        self.uni = self.Uni[suit.value]
        self.symbol = 'J'

    def give_value(self):
        return self.value

class QueenCard(PlayingCard):
    def __init__(self, suit):
        super().__init__()
        self.suit = suit
        self.value = 12
        self.uni = self.Uni[suit.value]
        self.symbol = 'Q'

    def give_value(self):
        return self.value

class KingCard(PlayingCard):
    def __init__(self, suit):
        super().__init__()
        self.suit = suit
        self.value = 13
        self.uni = self.Uni[suit.value]
        self.symbol = 'K'

    def give_value(self):
        return self.value

class AceCard(PlayingCard):
    def __init__(self, suit):
        super().__init__()
        self.suit = suit
        self.value = 14
        self.uni = self.Uni[suit.value]
        self.symbol = 'A'

    def give_value(self):
        return self.value


class Deck(object):
    def __init__(self):
        deck = np.array([])
        for j in range(0, 4):
            for i in range(2, 11):
                deck = np.append(deck, NumberedCard(i, Suit(j)))
            deck = np.append(deck, JackCard(Suit(j)))
            deck = np.append(deck, QueenCard(Suit(j)))
            deck = np.append(deck, KingCard(Suit(j)))
            deck = np.append(deck, AceCard(Suit(j)))
        self.deck = deck

    def shuffle_deck(self):
        np.random.shuffle(self.deck)

    def take_top_card(self):
        topcard = self.deck[-1]
        self.deck = np.delete(self.deck, -1)

        return topcard


class PlayerHand:
    """
    The playerhand class can be used to create a player hand. The hand may be given cards, have cards removed,
    sorted and evaluated for the best poker hand.
    """
    #data_changed = pyqtSignal()
    def __init__(self):
        self.cards = np.array([])

    def __eq__(self, other):
        return self.card_combo.value == other.card_combo.value and self.highcard == other.highcard

    def __lt__(self, other):
        if self.card_combo.value == other.card_combo.value:
            return self.highcard < other.highcard
        else:
            return self.card_combo.value < other.card_combo.value

    def __gt__(self, other):
        if self.card_combo.value == other.card_combo.value:
            return self.highcard > other.highcard
        else:
            return self.card_combo.value > other.card_combo.value

    def give_card(self, card):
        self.cards = np.append(self.cards, card)

    def remove_card(self, index):
        self.cards = np.delete(self.cards, index)

    def sort_cards(self):
        return np.sort(self.cards)


class PlayerHandModel(PlayerHand, QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        PlayerHand.__init__(self)
        QObject.__init__(self)
        self.card_combo = None
        self.active = 0
        self.marked_cards = [False]*len(self.cards)
        self.flipped_cards = True
        self.card_combo = PokerHand(self.cards)

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.data_changed.emit()


    def flipped(self, i):
        # This model only flips all or no cards, so we don't care about the index.
        # Might be different for other games though!
        return self.flipped_cards

    def give_card(self, card):
        super().give_card(card)
        self.data_changed.emit()

    def remove_card(self, index):
        super().remove_card(index)
        self.data_changed.emit()


    def best_poker_hand(self, cards):
        cards = np.append(self.cards, cards)
        value_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.card_combo = None
        suit_card_connector = [None]*14
        suit_count = [0, 0, 0, 0]

        for card in cards:
            val = card.value
            value_count[val-1] += 1
            suit = card.suit
            suit_count[suit.value] += 1
            suit_card_connector[val - 1] = card.suit


        v = self.check_straight_flush(suit_card_connector, suit_count)
        if v is not None:
            self.card_combo = v

        v = self.check_four_of_a_kind(value_count)
        if v is not None and self.card_combo is None:
            self.card_combo = v

        v = self.check_full_house(value_count)
        if v is not None and self.card_combo is None:
            self.card_combo = v

        v = self.check_flush(suit_count)
        if v is not None and self.card_combo is None:
            self.card_combo = v

        v = self.check_straight(value_count)
        if v is not None and self.card_combo is None:
            self.card_combo = v

        v = self.check_three_of_a_kind(value_count)
        if v is not None and self.card_combo is None:
            self.card_combo = v

        v = self.check_two_pair(value_count)
        if v is not None and self.card_combo is None:
            self.card_combo = v

        v = self.check_one_pair(value_count)
        if v is not None and self.card_combo is None:
            self.card_combo = v

        if self.card_combo is None:
            self.card_combo = CardCombo.highcard
            card_values_temp = np.sort(cards)
            card_vales = card_values_temp[-5:]


    @staticmethod
    def check_one_pair(value_count):
        if 2 in value_count:
            card_values = [value_count.index(2)+1]*2
            card_values[value_count.index(2)] = 0

            for j, data in reversed(list(enumerate(value_count))):
                if data != 0:
                    card_values.append([j+1]*data)

            return CardCombo.onepair, card_values[0:5]

    @staticmethod
    def check_two_pair(value_count):
        if value_count.count(2) >= 2:
            #lägg till det största paret först i card_values samt ta bort det för att kunna ta det näst högsta paret
            pairs = []
            single_cards = []
            for j, data in reversed(list(enumerate(value_count))):
                if data == 2:
                    pairs.append([j+1])
                elif data == 1:
                    single_cards.append([j+1])

            card_values = [pairs[:2],single_cards[0]]
            #lägg till det andra paret samt högsta kortet

            return CardCombo.twopair, card_values

    @staticmethod
    def check_three_of_a_kind(value_count):
        if 3 in value_count:

            single_cards = []
            for j, data in reversed(list(enumerate(value_count))):
                if data == 1:
                    single_cards.append([j + 1])
            card_values = [value_count.index(3) + 1] * 3 + [single_cards[:2]]
            return CardCombo.threeofakind, card_values

    @staticmethod
    def check_straight(value_count):
        n = 14
        next()
        if value_count[13] != 0:
            value_count[0] = 1
        for i in reversed(value_count):
            if n == 3:
                return
            if i != 0:
                if value_count[n - 1] != 0:
                    if value_count[n - 2] != 0:
                        if value_count[n - 3] != 0:
                            if value_count[n - 4] != 0:
                                card_values = [n]
                                return CardCombo.straight, card_values
            n -= 1

    @staticmethod
    def check_flush(suit_count, suit_card_connector):
        if max(suit_count) >= 5:
            card_values = []
            active_suit = suit_count.index(max(suit_count))
            for j, card in reversed(enumerate(suit_card_connector)):
                if card == active_suit:
                    card_values.append([j+1])

            return CardCombo.flush, card_values[:5]

    @staticmethod
    def check_full_house(value_count):
        if 3 in value_count:
            card_values = []
            for j, data in reversed(list(enumerate(value_count))):
                if data == 3:
                    card_values.append([j+1])
            if len(card_values) == 2:
                return CardCombo.fullhouse, card_values
            elif 2 in value_count:
                for j, data in reversed(list(enumerate(value_count))):
                    if data == 2:
                        card_values.append([j + 1])
                        return CardCombo.fullhouse, card_values

    @staticmethod
    def check_four_of_a_kind(value_count):
        if 4 in value_count:
            for j, data in reversed(list(enumerate(value_count))):
                if data in range(1, 4):
                    card_values = [value_count.index(4)+1, j+1]
                    return CardCombo.fourofakind, card_values


    @staticmethod
    def check_straight_flush(suit_card_connector, suit_count):
        if max(suit_count) >= 5:
            active_suit = suit_count.index(max(suit_count))
            if suit_card_connector[13] == active_suit:
                suit_card_connector[0] = active_suit
            for i, data in reversed(enumerate(suit_card_connector)):
                if i == 3:
                    return
                if data != 0:
                    if suit_card_connector[i-1] == active_suit:
                        if suit_card_connector[i-2] == active_suit:
                            if suit_card_connector[i-3] == active_suit:
                                if suit_card_connector[i-4] == active_suit:
                                    card_values = [i+1]
                                    return CardCombo.straightflush, card_values



class TableModel(PlayerHand, QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        PlayerHand.__init__(self)
        QObject.__init__(self)
        self.active = 0

    def flipped(self, i):       #since card_view.py will call this function, it is left in the code but without effect
        pass                    #this is instead of changing card_view.py to do differently for different input

    def give_card(self, card):
        super().give_card(card)
        self.data_changed.emit()

    def remove_card(self, index):
        super().remove_card(index)
        self.data_changed.emit()


class PokerHand:
    def __init__(self,highcard, cardcombo):
        self.highcard = HighCard(highcard)
        self.cardcombo = CardCombo(cardcombo)

j= PokerHand(3)
k=j.set_attributes(5, 4)
print(k)
print(type(k))
