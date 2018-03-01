
from Assignment_3 import poker

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
        self.stack=self.stack - amount

    def win(self, pot):
        self.stack = self.stack + pot

    def fold(self):
        self.cards = []


for i in range(0, NumberOfPlayers):
    player = Player(STARTINGSTACK, Playername[i])
    Players.append(player)

Players[1].win(200)
Players[1].bet(123)
print(Players[1].name, Players[1].stack, Players[1].cards)

#starta
CurrentBet = STARTINGBET
Deck = poker.Deck()
Deck.ShuffleDeck()

for i in range (0,2*NumberOfPlayers):
    Deck.TakeTopCard()


