from Hand import Hand

class Player:
    def __init__(self, initialBankroll, strategy, betting):
        self.hands: list[Hand] = []
        self.initialBankroll = initialBankroll
        self.rollingBankroll = initialBankroll
        self.strategy = strategy
        self.betting = betting
        self.totalWagered = 0

    def clearHand(self, hand: Hand):
        self.hands.remove(hand)

    def updateHand(self, hand: Hand):
        self.hands.append(hand)

    def splitPair(self, hand: Hand):
        splitHand = Hand([hand.splitHand()], hand.betSize)
        self.updateHand(splitHand)
        return splitHand

    def getInitialHand(self):
        return self.hands[0]