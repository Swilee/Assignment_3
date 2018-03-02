
import poker, Assignment_3_Andreasson_Edman
import numpy as np
#setup

pot = 0
NumberOfPlayers = int(input('Number of players:'))
Playername=[None]*NumberOfPlayers
for i in range(0, NumberOfPlayers):
    Playername[i] = input('Player %d name:' % (i+1))

STARTINGSTACK = float(input('Set starting stack amount:'))
STARTINGBET = float(input('Set starting bet:'))
ActivePlayers = NumberOfPlayers
Players = []
class Player(object):
    def __init__(self, startingstack, playername):
        self.stack = startingstack
        self.name = playername
        self.cards = []
        self.hand = []

    def bet(self, amount):

        if amount > self.stack:
            print('error, you cant bet more than you have')
        else:
            self.stack = self.stack - amount
            self.new_stack.emit()

    def win(self, pot):
        self.stack = self.stack + pot
        self.new_stack.emit()

    def fold(self):
        self.cards = []


for i in range(0, NumberOfPlayers):
    player = Player(STARTINGSTACK, Playername[i])
    Players.append(player)

#starta
CurrentBet = STARTINGBET
Deck = poker.Deck()
Deck.ShuffleDeck()

for i in range(0, 2*NumberOfPlayers):
    card = Deck.TakeTopCard()
    print(card.symbol)
    if i > NumberOfPlayers-1:
        Players[i-NumberOfPlayers].cards = np.append(Players[i-NumberOfPlayers].cards, card)
    else:
        Players[i].cards = np.array([card])

print(Players[0].cards[0], Players[0].cards[1])
print(Players[1].cards[0], Players[1].cards[1])


Assignment_3_Andreasson_Edman.game.show()
#qt_app.exec_()

Assignment_3_Andreasson_Edman.app.exec_()


