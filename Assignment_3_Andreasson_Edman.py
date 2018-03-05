from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
import sys
from Assignment_3 import card_view  # poker, pokergame


CurrentBet = 0

app=QApplication(sys.argv)

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
        '''
        if self.checkbutton.isChecked():
            self.check_press.emit()

        if self.betbutton.isChecked():
            self.bet_press.emit()

        if self.foldbutton.isChecked():
            self.fold_press.emit()
        '''

        #self.hbox = hbox


    def Create_GUI(self,player1,player2,table,btn):

            final = QVBoxLayout()
            final.layout().addWidget(btn)
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
        self.player.new_stack.connect(self.update_stack)
        self.update_stack()

    def update_stack(self):
        self.stack.setText('%d $' % self.player.stack)


class Tablewindow(QGroupBox):
    check_press = pyqtSignal()
    bet_press = pyqtSignal()
    fold_press = pyqtSignal()
    def __init__(self, table):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(card_view.CardView(table.hand))
        self.table = table
        self.pot = QLabel()
        self.layout().addWidget(self.pot)
        self.CurrentBet = QLabel()
        self.layout().addWidget(self.CurrentBet)
        #self.checkbutton = QPushButton('Check')
        #self.foldbutton = QPushButton("Fold")
        #self.betbutton = QPushButton("Bet")

        #self.layout().addWidget(self.checkbutton)
        #self.layout().addWidget(self.betbutton)
        #self.layout().addWidget(self.foldbutton)
        self.update_current_bet()
        self.update_pot()


    def update_current_bet(self):
        self.CurrentBet.setText('Current bet: %d $' % self.table.CurrentBet)
        self.check_press.emit()

    def update_pot(self):
        self.pot.setText('Pot: %d $' % self.table.Pot)

    def checkbutton_clicked(self):
        self.check_press.emit()

        self.checkbutton.clicked.connect(self.update_current_bet())

class Buttons(QGroupBox):
    check_press = pyqtSignal()
    bet_press = pyqtSignal()
    fold_press = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.checkbutton = QPushButton('Check')
        self.foldbutton = QPushButton("Fold")
        self.betbutton = QPushButton("Bet")
        self.setLayout(QVBoxLayout())

        self.layout().addWidget(self.checkbutton)
        self.layout().addWidget(self.foldbutton)
        self.hello()
        self.foldbutton.clicked.connect(self.check_press.emit)
        self.checkbutton.clicked.connect(self.hello)
    def hello(self):
        print('Check')
        self.check_press.emit()



