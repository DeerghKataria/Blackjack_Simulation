from Card import Card
from Deck import Deck
from Hand import Hand

class Dealer:
    def __init__(self, numDecks: int, penetration, strategy):
        self.deck = Deck(numDecks)
        self.hand: Hand = None
        self.upCard: Card = None
        self.penetration = penetration / self.deck.numDecks
        self.strategy = strategy

    def dealCard(self):
        dealtCard = self.deck.drawCard()
        return dealtCard
    
    def updateHand(self, hand: Hand):
        self.hand = hand
        
    def clearHand(self):
        self.hand = None

    def setUpCard(self, upcard: Card):
        self.upCard = upcard

    def shuffleDeck(self):
        self.deck.resetDeck()

    def discardDealerHand(self):
        for card in self.hand.cards:
            self.deck.discardCard(card)
        self.card = None
        self.upCard = None

    def discardPlayerHand(self, hand: Hand):
        for card in hand.cards:
            self.deck.discardCard(card)
            
    def offerInsurance(self):
        return self.upCard.getValue() == 11
    
    def penetrationReached(self):
        return self.deck.getPenetration() <= self.penetration
    
    def getDecksRemaining(self):
        return round(len(self.deck.drawPile) / 52)