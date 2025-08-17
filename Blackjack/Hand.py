from Card import Card, Suit

class Hand:
    def __init__(self, cards: list[Card], betSize: int):
        self.cards = cards
        self.betSize = betSize
        self.insuranceBet = 0
        self.isInsured = False
        self.isDoubled = False
        self.isSplit = False
        self.action = None
        self.finalValue = 0

    def getHandValue(self, softAceCount):
        value = 0

        for card in self.cards:
            cardValue = card.getValue()
            value += cardValue

        handValue = value - (softAceCount * 10)

        return handValue
    
    def getSoftTotal(self):
        value = 0
        for card in self.cards:
            cardValue = card.getValue()
            value += cardValue

        return value

    def isBlackjack(self):
        if len(self.cards) != 2:
            return False
        handValue = self.getSoftTotal()
        return handValue == 21

    def isBust(self, softAceCount):
        return self.getHandValue(softAceCount) > 21
    
    def isPair(self):
        if len(self.cards) != 2:
            return False
        card1Rank = self.cards[0].getRank()
        card2Rank = self.cards[1].getRank()
        return card1Rank == card2Rank
    
    def doubleDown(self):
        self.betSize = self.betSize * 2
        self.isDoubled = True

    def splitHand(self):
        return self.cards.pop()

    def insureHand(self):
        self.insuranceBet = self.betSize / 2
        self.isInsured = True

    def getAceCount(self):
        aces = 0
        for card in self.cards:
            if card.getValue() == 11:
                aces += 1
        return aces
    
    def printHand(self):
        printHand = []
        for card in self.cards:
            printHand.append(card.printCard())
        return printHand