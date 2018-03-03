#line 120
def mousePressEvent(self, event):
    # We can check which item, if any, that we clicked on by fetching the scene items (neat!)
    pos = self.mapToScene(event.pos())
    item = self.scene.itemAt(pos, self.transform())
    if item is not None:
        # Report back that the user clicked on the card at given position:
        # The model can choose to do whatever it wants with this information.
        self.model.clicked_position(item.position)


# line 140
class MySimpleCard:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit


# You have made a class similar to this (hopefully):
class Hand:
    def __init__(self):
        # Lets use some hardcoded values for most of this to start with
        self.cards = [MySimpleCard(13, 2), MySimpleCard(7, 0), MySimpleCard(13, 1)]

    def add_card(self, card):
        self.cards.append(card)


class HandModel(Hand, QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        Hand.__init__(self)
        QObject.__init__(self)

        # Additional state needed by the UI, keeping track of the selected cards:
        self.marked_cards = [False]*len(self.cards)
        self.flipped_cards = True

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.data_changed.emit()

    def marked(self, i):
        return self.marked_cards[i]

    def flipped(self, i):
        # This model only flips all or no cards, so we don't care about the index.
        # Might be different for other games though!
        return self.flipped_cards

    def clicked_position(self, i):
        # Mark the card as position "i" to be thrown away
        self.marked_cards[i] = not self.marked_cards[i]
        self.data_changed.emit()

    def add_card(self, card):
        super().add_card(card)
        self.data_changed.emit()
