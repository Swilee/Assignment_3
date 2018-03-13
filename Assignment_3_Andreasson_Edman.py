from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
import sys
from Assignment_3 import card_view, pokergame


class Tablescene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.tile = QPixmap('table.png')
        self.setBackgroundBrush(QBrush(self.tile))


class PokerWindow(QWidget):
    '''
    PokerWindow represents the main window
    '''

    #def __init__(self, player1, player2, table, btn):
    def __init__(self, game):
        #self.scene = Tablescene()
        #super().__init__(self.scene)
        super().__init__()
        final = QVBoxLayout()
        final.addWidget(TableWindow(game.table))
        final.layout().addWidget(Buttons(game))
        final.addWidget(PlayerWindow(game.players))
        final.addWidget(PlayerWindow(game.players[1]))
        #final.addWidget(game.players[1])
        #final.scene = self.scene
        self.setLayout(final)
        self.setGeometry(400, 100, 600, 500)
        self.setWindowTitle("Texas Hold'em")

        self.game.game_message.connect(self.present_message)

        #self.game_ended.connect(self.close)

    def present_message(self, s):
        #self.eventWidget.addLine(s)
        QMessageBox.information(QMessageBox(), 'Message', s)


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
        self.change_player.connect(self.change_active_player)

    def change_active_player(self):
        if self.player.active == 1:
            self.active.setText('Your turn')
        else:
            self.active.setText('Waiting for other player')

    def update_stack(self):
        self.stack.setText('$%d' % self.player.stack)


class TableWindow(QGroupBox):

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
    def __init__(self, game):
        super().__init__()
        self.checkbutton = QPushButton('Check/Call')
        self.foldbutton = QPushButton("Fold")
        self.betbutton = QPushButton("Bet")
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.checkbutton)
        self.layout().addWidget(self.foldbutton)
        self.layout().addWidget(self.betbutton)


        def read_and_pass_bet():
            min_bet, max_bet = game.compute_bet_limit()
            amount, ok = QInputDialog.getInt(self, 'Bet', 'Enter bet (min = %d, max = %d)' % (
                min_bet, max_bet), min=min_bet, max=max_bet)
            game.bet(int(amount))

        self.betbutton.clicked.connect(read_and_pass_bet)
        self.foldbutton.clicked.connect(game.fold)
        self.checkbutton.clicked.connect(game.check_or_call)


app = QApplication(sys.argv)

window = PokerWindow(pokergame.GameMaster())
window.show()

app.exec_()
