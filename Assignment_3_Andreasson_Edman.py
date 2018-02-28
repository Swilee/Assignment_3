from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
qt_app = QApplication(sys.argv)


class PokerWindow(QGroupBox):
    ''' PokerWindow represents the five cards put on the table and the player options '''
    def __init__(self):
        super().__init__("Poker content")
        pot = QGroupBox('pot=%d' % 123451)
        checkbutton = QPushButton("Check/Call")
        foldbutton = QPushButton("Fold")
        betbutton = QPushButton("Bet")
        card1 = QPushButton("kort1")
        card2 = QPushButton("kort2")
        card3 = QPushButton("kort3")
        card4 = QPushButton("kort4")
        card5 = QPushButton("kort5")

        vbox = QVBoxLayout()
        vbox.addWidget(pot)
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

        player1box = QHBoxLayout()
        player1card1 = QPushButton("första")
        player1card2 = QPushButton("andra")

        player2card1 = QPushButton("första")
        player2card2 = QPushButton("andra")

        Playername1 = QGroupBox('Player: %s' % 'Alex')
        Playername2 = QGroupBox('Player: %s' % 'Edman')

        player1box.addWidget(player2card1)
        player1box.addWidget(player2card2)
        player1box.addWidget(Playername1)

        player2box = QHBoxLayout()
        player2box.addWidget(player1card1)
        player2box.addWidget(player1card2)
        player2box.addWidget(Playername2)


        final=QVBoxLayout()
        final.addLayout(hbox)
        final.addLayout(player1box)
        final.addLayout(player2box)

        self.setLayout(final)
        self.setGeometry(600, 300, 300, 150)
        self.setWindowTitle('Texas Holdem')


game = PokerWindow()
game.show()
qt_app.exec_()
