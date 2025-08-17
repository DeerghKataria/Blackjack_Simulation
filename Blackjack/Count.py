from Card import Card

class HiLoCount:
    def __init__(self):
        self.runningCount = 0

    def updateCount(self, card):
        value = card.getValue()
        if 2 <= value <= 6:
            self.runningCount += 1
        elif (value == 10 or value == 11):
            self.runningCount -= 1

    def resetCount(self):
        self.runningCount = 0
        
    def getTrueCount(self, decksRemaining):
        return round(self.runningCount / decksRemaining)