from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *

CurrentBet = 0
import sys
qt_app = QApplication(sys.argv)

class Tablescene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.tile = QPixmap('table.png')
        self.setBackgroundBrush(QBrush(self.tile))


class PokerWindow(QGraphicsView):
    ''' PokerWindow represents the five cards put on the table and the player options '''
    def __init__(self):
        #super().__init__("Poker content")

        self.scene = Tablescene()
        super().__init__(self.scene)

        Potlabel = QLabel('Pot = %d $' % 123451)
        CurrentBetLabel = QLabel('Current bet = %d $' %1)
        if CurrentBet==0:
            checkbutton = QPushButton("Check")
        else:
            checkbutton = QPushButton("Call")

        foldbutton = QPushButton("Fold")
        betbutton = QPushButton("Bet")
        card1 = QPushButton("kort1")
        card2 = QPushButton("kort2")
        card3 = QPushButton("kort3")
        card4 = QPushButton("kort4")
        card5 = QPushButton("kort5")

        vbox = QVBoxLayout()
        vbox.addWidget(Potlabel)
        vbox.addWidget(CurrentBetLabel)
        vbox.addWidget(checkbutton)
        vbox.addWidget(foldbutton)
        vbox.addWidget(betbutton)
        vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(card1)
        hbox.addWidget(card2)
        hbox.addWidget(card3)
        hbox.addWidget(card4)
        hbox.addWidget(card5)
        hbox.addStretch(1)
        hbox.addLayout(vbox)


        player1box = QGroupBox('Player')
        player1box.setLayout(QHBoxLayout())
        player1card1 = QPushButton("första")
        player1card2 = QPushButton("andra")

        player2card1 = QPushButton("första")
        player2card2 = QPushButton("andra")

        Playername1 = QLabel('%s : %d $' % (input('Name?'), 500))
        Playername2 = QLabel('%s : %d $' % ('Edman', 200))



        player1box.layout().addWidget(player2card1)
        player1box.layout().addWidget(player2card2)
        player1box.layout().addWidget(Playername1)


        player2box = QGroupBox('Player')
        player2box.setLayout( QHBoxLayout())
        player2box.layout().addWidget(player1card1)
        player2box.layout().addWidget(player1card2)
        player2box.layout().addWidget(Playername2)



        final=QVBoxLayout()
        final.addLayout(hbox)
        final.addWidget(player1box)
        final.addWidget(player2box)


        self.setLayout(final)
        self.setGeometry(600, 300, 300, 150)
        self.setWindowTitle('Texas Holdem')

class Playerwindow(QGraphicsView):
    def __init__(self, startingstack, playername, cards):
        self.name = playername
        self.cards = cards
        self.stack = startingstack
        self.box = QGroupBox('Player')
        self.box.setLayout(QHBoxLayout())
        self.box.layout().addWidget(self.cards)
        self.box.layout().addWidget(QLabel('%s %d $' % self.name, self.stack))

app = QApplication(sys.argv)
game = PokerWindow()

