from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
import sys
from Assignment_3 import card_view  # poker, pokergame


class Tablescene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.tile = QPixmap('table.png')
        self.setBackgroundBrush(QBrush(self.tile))


class PokerWindow(QGraphicsView):
    '''
    PokerWindow represents the main window
    '''
    def __init__(self,player1, player2, table, btn):
        self.scene = Tablescene()
        super().__init__(self.scene)
        final = QVBoxLayout()
        final.addWidget(table)
        final.layout().addWidget(btn)
        final.addWidget(player1)
        final.addWidget(player2)
        final.scene = self.scene
        self.setLayout(final)
        self.setGeometry(400, 100, 600, 500)
        self.setWindowTitle("Texas Hold'em")


class PlayerWindow(QGroupBox):
    def __init__(self, player):
        super().__init__(player.name)
        self.player = player
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(card_view.CardView(player.hand))
        self.stack = QLabel()
        self.layout().addWidget(self.stack)
        self.player.new_stack.connect(self.update_stack)
        self.active = QLabel()
        self.layout().addWidget(self.active)
        self.update_stack()

    def update_stack(self):
        self.stack.setText('%d $' % self.player.stack)

    def set_to_active(self):
        self.active.setText('Your turn')

    def set_to_inactive(self):
        self.active.setText('Waiting for other player')



class TableWindow(QGroupBox):
    quitter = pyqtSignal()
    def __init__(self, table):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(card_view.CardView(table.hand))
        self.table = table
        self.pot = QLabel()
        self.CurrentBet = QLabel()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.pot)
        self.vbox.addWidget(self.CurrentBet)
        self.layout().addLayout(self.vbox)
        self.update_pot_and_bet()
        self.table.new_pot_or_bet.connect(self.update_pot_and_bet)

    def update_pot_and_bet(self):
        self.pot.setText('Pot: %d $' % self.table.Pot)
        self.CurrentBet.setText('Current bet: %d $' % self.table.CurrentBet)


class Buttons(QGroupBox):
    def __init__(self):
        super().__init__()
        self.checkbutton = QPushButton('Check/Call')
        self.foldbutton = QPushButton("Fold")
        self.betbutton = QPushButton("Bet")
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.checkbutton)
        self.layout().addWidget(self.foldbutton)
        self.layout().addWidget(self.betbutton)


CurrentBet = 0
app = QApplication(sys.argv)
