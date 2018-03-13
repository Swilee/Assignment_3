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
    """
    The JackCard class represents the jack card
    """
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

        #self.pokerhand = PokerHand(cardcombo.v, card_values)

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

        suit_card_connector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        suit_count = [0, 0, 0, 0]

        for card in cards:
            val = card.value
            value_count[val-1] += 1
            suit = card.suit
            suit_count[suit.value] += 1

        if max(suit_count) >= 5:
            for card in cards:
                if card.suit.value == suit_count.index(max(suit_count)):
                    suit_card_connector[card.value - 1] = 1

        v, card_values = self.check_straight_flush(suit_card_connector, suit_count)
        if v is not None:

            self.card_combo = v
            self.card_values = card_values

        if self.card_combo is None:
            v, card_values = self.check_four_of_a_kind(value_count)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            v, card_values = self.check_full_house(value_count)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            v, card_values = self.check_flush(suit_count, suit_card_connector)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            v, card_values = self.check_straight(value_count)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            v, card_values = self.check_three_of_a_kind(value_count)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            v , card_values = self.check_two_pair(value_count)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values

        if self.card_combo is None:
            v, card_values = self.check_one_pair(value_count)
            if v is not None:
                self.card_combo = v
                self.card_values = card_values


        if self.card_combo is None:
            self.card_combo, self.card_values = self.high_card(value_count)


        self.pokerhand = PokerHand(self.card_combo, self.card_values)





    @staticmethod
    def high_card(value_count):
        ''' Checks for the 5 highest cards in a pokerhand
        :param value_count: list containing the how many of each card is in the hand
        :return  list of the 5 highest cards
        '''
        card_values = []
        for j, data in reversed(list(enumerate(value_count))):
            if data == 1:
                card_values.append(j + 1)
        return 0, card_values[0:5]

    @staticmethod
    def check_one_pair(value_count):
        '''
        Checks for a pair in a pokerhand
        :param value_count: list containing the how many of each card is in the hand
        :return  None if no pair is found, else 1 ( value of a pair) and a list with the
        pair and the 3 highest cards exluding the pair
        '''
        if 2 in value_count:
            card_values = [value_count.index(2)+1]
            for j, data in reversed(list(enumerate(value_count))):
                if data == 1:
                    card_values.append(j+1)

            return 1, card_values[0:4]
        else:
            return None, None
    @staticmethod
    def check_two_pair(value_count):
        '''
        Checks for the highest two pair in a pokerhand
        :param value_count: list containing the how many of each card is in the hand
        :return  None if no two pair is found, else 2 ( the value of a two pair) and
        a list with the pairs and the highest card exluding the two pair
        '''
        if value_count.count(2) >= 2:
            #lägg till det största paret först i card_values samt ta bort det för att kunna ta det näst högsta paret
            pairs = []
            single_cards = []
            for j, data in reversed(list(enumerate(value_count))):
                if data == 2:
                    pairs.append(j+1)
                elif data == 1:
                    single_cards.append(j+1)
            card_values = pairs[:2]
            if pairs[-1] == card_values[-1]:
                card_values.append(single_cards[0])
            else:
                card_values.append(max(single_cards[0], pairs[2]))

            return 2, card_values
        else:
            return None, None


    @staticmethod
    def check_three_of_a_kind(value_count):
        '''
        Checks for a three of a kind in a pokerhand
        :param value_count: list containing the how many of each card is in the hand
        :return  None if no two pair is found, else 3 ( the value of a three of a kind) and
        a list with the pairs and the twp highest cards exluding the three of a kind
        '''
        if 3 in value_count:
            single_cards = []
            for j, data in reversed(list(enumerate(value_count))):
                if data == 1:
                    single_cards.append(j + 1)
            card_values = [value_count.index(3) + 1,  single_cards[0], single_cards[1]]
            return 3, card_values
        else:
            return None, None

    @staticmethod
    def check_straight(value_count):
        ''' Checks for the highest straight in a pokerhand
        :param value_count: list containing the how many of each card is in the hand
        :return  None if no two pair is found, else 4 ( the value of a two pair) and
        the highest card in the straight'''
        n = 13
        if value_count[13] != 0:
            value_count[0] = 1
        for i in reversed(value_count):
            if n == 3:
                return None, None
            if i != 0:
                if value_count[n - 1] != 0:
                    if value_count[n - 2] != 0:
                        if value_count[n - 3] != 0:
                            if value_count[n - 4] != 0:
                                card_values = [n+1]
                                return 4, card_values
            n -= 1

    @staticmethod
    def check_flush(suit_count, suit_card_connector):
        ''' Checks for the highest flush in a pokerhand
        :param suit_count: number of cards of each suit
        :param suit_card_connector: list containing how many of each card with the most common suit
        is in the hand
        :return  None if no flush is found, else 5 ( the value of a flush) and a list of the five
         highest cards in the flush
        '''
        if max(suit_count) >= 5:
            card_values = []
            for j, card in reversed(list(enumerate(suit_card_connector))):
                if card:
                    card_values.append(j+1)
            return 5, card_values[:5]
        else:
            return None, None

    @staticmethod
    def check_full_house(value_count):
        ''' Checks for the best full house in a pokerhand
                 :param value_count: list containing the how many of each card is in the hand
                 :return  None if no full house is found, else 6 ( the value of a full house) and
                 a list with the three of a kind and the pair'''
        if 3 in value_count:
            card_values = []
            for j, data in reversed(list(enumerate(value_count))):
                if data == 3:
                    card_values.append(j+1)
            if len(card_values) == 2:
                return 6, card_values
            elif 2 in value_count:
                for j, data in reversed(list(enumerate(value_count))):
                    if data == 2:
                        card_values.append(j + 1)
                        return 6, card_values
            else:
                return None, None
        else:
            return None, None

    @staticmethod
    def check_four_of_a_kind(value_count):
        ''' Checks for a four of a kind in a pokerhand
                 :param value_count: list containing the how many of each card is in the hand
                 :return  None if no four of a kind is found, else 7 ( the value of a two pair) and
                 a list with the four of a kind and the highest card exluding the four of a kind
                 '''
        if 4 in value_count:
            for j, data in reversed(list(enumerate(value_count))):
                if data in range(1, 4):
                    card_values = [value_count.index(4)+1, j+1]
                    return 7, card_values
        else:
            return None, None



    @staticmethod
    def check_straight_flush(suit_card_connector, suit_count):
        ''' Checks for the highest straight flush in a pokerhand
        :param suit_count: number of cards of each suit
        :param suit_card_connector: list containing how many of each card with the most common suit
        is in the hand
        :return  None if no straight flush is found, else 8 ( the value of a straight flush) and
                 the highest card in the straight flush
        '''
        if max(suit_count) >= 5:
            if suit_card_connector[13]:
                suit_card_connector[0] = True
            for i, data in reversed(list(enumerate(suit_card_connector))):
                if i == 3:
                    return None, None
                if data != 0:
                    if suit_card_connector[i-1]:
                        if suit_card_connector[i-2]:
                            if suit_card_connector[i-3]:
                                if suit_card_connector[i-4]:
                                    card_values = [i+1]
                                    return 8, card_values
        else:
            return None, None


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
    def __gt__(self, other):
        if self.cardcombo.value == other.cardcombo.value:
            for i, data in enumerate(self.highcard):
                if data.value != other.highcard[i].value:
                    return data.value > other.highcard[i].value
        else:
            return self.cardcombo.value > other.cardcombo.value

    def __lt__(self, other):
        if self.cardcombo.value == other.cardcombo.value:
            for i, data in enumerate(self.highcard):
                if data.value != other.highcard[i].value:
                    return data.value < other.highcard[i].value
        else:
            return self.cardcombo.value < other.cardcombo.value

    def __init__(self, cardcombo, highcard):
        self.highcard = []
        self.cardcombo = CardCombo(cardcombo)
        print(self.cardcombo)
        for value in highcard:
            self.highcard.append(HighCard(value))





