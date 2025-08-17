from Card import Card, Suit
import random

class Deck:
    def __init__(self, numDecks):
        self.numDecks = numDecks
        self.Discard = []
        self.drawPile = []
        for deck in range(0, numDecks):
            for suit in Suit.Clubs, Suit.Spades, Suit.Diamonds, Suit.Hearts:
                for rank in range (1, 14):
                    self.drawPile.append(Card(rank, suit))

    def printDeck(self):
        for card in self.drawPile:
            print(card.printCard())

    def drawCard(self):
        return self.drawPile.pop(0)
    
    def discardCard(self, card):
        self.Discard.append(card)

    def resetDeck(self):
        # for card in self.Discard:
        #     self.drawPile.append(card)
        # self.Discard = []
        self.drawPile = []
        for deck in range(0, self.numDecks):
            for suit in Suit.Clubs, Suit.Spades, Suit.Diamonds, Suit.Hearts:
                for rank in range (1, 14):
                    self.drawPile.append(Card(rank, suit))
        random.shuffle(self.drawPile)
        
    def getPenetration(self):
        return len(self.drawPile) / (self.numDecks * 52)