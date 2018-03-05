from Assignment_3 import Assignment_3_Andreasson_Edman
from Assignment_3 import poker, card_view
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *

import sys
#setup




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
    def __init__(self, startingstack, playername):
        super().__init__()
        self.stack = startingstack
        self.name = playername
        self.cards = []
        self.hand = poker.Playerhandmodel()
        self.active = 1
        btn = Assignment_3_Andreasson_Edman.Buttons()
        btn.check_press.connect(self.remove_player)
        #self.dsadsa=Assignment_3_Andreasson_Edman.Buttons().a
        #self.connect(Assignment_3_Andreasson_Edman.Buttons().a, self.SIGNAL('clicked()'), self.remove_player())
        #self.sda = Assignment_3_Andreasson_Edman.Tablewindow().foldbutton
        #self.sda.check_press.connect(self.remove_player)
        #Assignment_3_Andreasson_Edman.Tablewindow().checkbutton.connect(self.remove_player())
    def bet(self, amount):

        self.stack = self.stack - amount
        self.new_stack.emit()

    def win(self, pot):
        self.stack = self.stack + pot
        self.new_stack.emit()

    def fold(self):
        self.hand.cards = []

        self.player_fold.emit()
        self.active = 0


    def remove_player(self):
        print('button got pressed')



class Table(QObject):
    def __init__(self, currentbet, pot):
        super().__init__()
        self.CurrentBet = currentbet
        self.Pot = pot
        self.hand = poker.TableModel()


for i in range(0, NumberOfPlayers):
    player = Player(STARTINGSTACK, Playername[i])
    Players.append(player)

#starta
CurrentBet = STARTINGBET
Deck = poker.Deck()
Deck.ShuffleDeck()
print('ok')
for i in range(0, 2*NumberOfPlayers):
    card = Deck.TakeTopCard()
    if i > NumberOfPlayers-1:
        Players[i-NumberOfPlayers].hand.givecard(card)
    else:
        Players[i].hand.givecard(card)




print('ok')
app = Assignment_3_Andreasson_Edman.QApplication(sys.argv)

print('ok')

table = Table(CurrentBet, pot)

print('ok')

tablebox = Assignment_3_Andreasson_Edman.Tablewindow(table)
#tablebox.checkbutton.clicked.connect(print('button was pressed'))
player1box = Assignment_3_Andreasson_Edman.Playerwindow(Players[0])
print('ok')
player2box = Assignment_3_Andreasson_Edman.Playerwindow(Players[1])
print('ok')
btn=Assignment_3_Andreasson_Edman.Buttons()
game = Assignment_3_Andreasson_Edman.PokerWindow()
print('ok')
game.Create_GUI(player1box, player2box, tablebox, btn)

game.show()

for i in range (3):
    card = Deck.TakeTopCard()
    table.hand.givecard(card)





app.exec_()




#game = Assignment_3_Andreasson_Edman.PokerWindow()
#game.show()


