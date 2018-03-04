from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *

from Assignment_3 import card_view, poker


CurrentBet = 0



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

        vbox = QHBoxLayout()
        vbox.addWidget(Potlabel)
        vbox.addWidget(CurrentBetLabel)
        vbox.addWidget(checkbutton)
        vbox.addWidget(foldbutton)
        vbox.addWidget(betbutton)
        vbox.addStretch(1)

        self.vbox = vbox


        #self.hbox = hbox


    def Create_GUI(self,player1,player2,table):

            final = QVBoxLayout()
            final.addLayout(self.vbox)
            final.addWidget(table)
            final.addWidget(player1)
            final.addWidget(player2)

            self.setLayout(final)
            self.setGeometry(600, 300, 300, 150)
            self.setWindowTitle('Texas Holdem')


class Playerwindow(QGroupBox):
    def __init__(self, player):
        super().__init__(player.name)
        self.player = player
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(card_view.CardView(player.hand))
        self.stack = QLabel()
        self.layout().addWidget(self.stack)
       # self.player.new_stack.connect(self.update_stack)
        self.update_stack()

    def update_stack(self):
        self.stack.setText('%d $' % self.player.stack)

class Tablewindow(QGroupBox):
    def __init__(self, table):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(card_view.CardView(table))


#app = QApplication(sys.argv)
#game = PokerWindow()
#game.show()
#app.exec_()






