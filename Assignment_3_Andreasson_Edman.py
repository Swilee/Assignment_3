from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
qt_app = QApplication(sys.argv)


class PokerWindow(QGroupBox):
    ''' PokerWindow represents the five cards put on the table and the player options '''
    def __init__(self):
        super().__init__("Poker content")

        checkbutton = QPushButton("Check/Call")
        foldbutton = QPushButton("Fold")
        betbutton = QPushButton("Bet")

        hbox = QHBoxLayout()

        hbox.addStretch(1)
        hbox.addWidget(checkbutton)
        hbox.addWidget(foldbutton)
        hbox.addWidget(betbutton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(QLabel('Buttons:'))
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(600, 300, 300, 150)
        self.setWindowTitle('Texas Holdem')


game = PokerWindow()
game.show()
qt_app.exec_()
