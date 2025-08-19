from Hand import Hand
import random

class StrategyFormat:
    def __init__(self, isCounting, strategyAccuracy, count, HouseRules):
        pass
    
    def hardTotalAction(self, hand, dealerUpCard, softAceCount, count, decksRemaining):
        pass
    
    def softTotalAction(self, hand, dealerUpCard, softAceCount, count):
        pass
    
    def shouldSplit(self, hand, dealerUpCard, count, decksRemaining):
        pass
    
    def shouldSurrender(self, hand, dealerUpCard, count, decksRemaining):
        pass
    
    def takeInsurance(self, count, decksRemaining):
        pass
    
    
class RandomStrategy(StrategyFormat):
    def __init__(self, isCounting, strategyAccuracy, count, HouseRules):
        self.isCounting = isCounting
        self.strategyAccuracy = strategyAccuracy
        self.HouseRules = HouseRules
    
    def hardTotalAction(self, hand, dealerUpCard, softAceCount, count, decksRemaining=None):
        return random.choice(['H', 'D', 'S'])
    
    def softTotalAction(self, hand, dealerUpCard, softAceCount, count):
        return random.choice(['H', 'D', 'S'])
    
    def shouldSplit(self, hand, dealerUpCard, count, decksRemaining=None):
        return random.choice([True, False])
    
    def shouldSurrender(self, hand, dealerUpCard, count, decksRemaining=None):
        return False
    
    def takeInsurance(self, count, decksRemaining):
        return random.choice([True, False])
    
    
class NoBustStrategy(StrategyFormat):
    def __init__(self, isCounting, strategyAccuracy, count, HouseRules):
        self.isCounting = isCounting
        self.strategyAccuracy = strategyAccuracy
        self.HouseRules = HouseRules
    
    def hardTotalAction(self, hand, dealerUpCard, softAceCount, count, decksRemaining):
        handValue = hand.getHandValue(softAceCount)
        if handValue < 12:
            return 'H'
        return 'S'
    
    def softTotalAction(self, hand, dealerUpCard, softAceCount, count):
        return 'H'
    
    def shouldSplit(self, hand, dealerUpCard, count, decksRemaining):
        return False
    
    def shouldSurrender(self, hand, dealerUpCard, count, decksRemaining):
        return False
    
    def takeInsurance(self, count, decksRemaining):
        return False
  
      
class CasinoStrategy(StrategyFormat):
    def __init__(self, isCounting, strategyAccuracy, count, HouseRules):
        self.isCounting = isCounting
        self.strategyAccuracy = strategyAccuracy
        self.HouseRules = HouseRules
    
    def hardTotalAction(self, hand, dealerUpCard, softAceCount, count, decksRemaining=None):
        handValue = hand.getHandValue(softAceCount)
        if handValue < 17:
            return 'H'
        else:
            return 'S'
    
    def softTotalAction(self, hand, dealerUpCard, softAceCount, count):
        handValue = hand.getHandValue(softAceCount)
        if self.HouseRules.standS17 == True:
            if handValue < 17:
                return 'H'
            else:
                return 'S'
        else:
            if handValue <= 17:
                return 'H'
            else:
                return 'S'
    
    def shouldSplit(self, hand, dealerUpCard, count, decksRemaining=None):
        return False
    
    def shouldSurrender(self, hand, dealerUpCard, count, decksRemaining=None):
        return False
    
    def takeInsurance(self, count, decksRemaining=None):
        return False
    
    
class BasicStrategyS17(StrategyFormat):
    def __init__(self, isCounting, strategyAccuracy, count, HouseRules):
        self.isCounting = isCounting
        self.strategyAccuracy = strategyAccuracy
        self.HouseRules = HouseRules
        
        self.decisionSplitting = {
            #     A     2     3     4     5     6     7     8     9     10
            1: [True, True, True, True, True, True, True, True, True, True],
            10: [False, False, False, False, False, False, False, False, False, False],
            9: [False, True, True, True, True, True, False, True, True, False],
            8: [True, True, True, True, True, True, True, True, True, True],
            7: [False, True, True, True, True, True, True, False, False, False],
            6: [False, True, True, True, True, True, False, False, False, False],
            5: [False, False, False, False, False, False, False, False, False, False],
            4: [False, False, False, False, True, True, False, False, False, False],
            3: [False, True, True, True, True, True, True, False, False, False],
            2: [False, True, True, True, True, True, True, False, False, False]
        }
        
        self.decisionSoftTotal = {
            #     A    2    3    4    5    6    7    8    9    10
            21: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            18: ['H', 'S', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H'],
            17: ['H', 'H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],
            16: ['H', 'H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],
            15: ['H', 'H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],
            14: ['H', 'H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H'],
            13: ['H', 'H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H'],
            11: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
        }
        
        self.decisionHardTotal = {
            #     A    2    3    4    5    6    7    8    9    10
            17: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            16: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],
            15: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],
            14: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],
            13: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],
            12: ['H', 'H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],
            11: ['H', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],
            10: ['H', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'],
            9: ['H', 'H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],
            8: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
        }
        
        self.decisionSurrender = {
            16: [True, False, False, False, False, False, False, False, True, True],
            15: [False, False, False, False, False, False, False, False, False, True]
        }
        
        if HouseRules.DASoffered == False:
            self.DASdeviations()
            
        if HouseRules.LSoffered == True:
            self.decisionHardTotal.update({16: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S']})
        
    def DASdeviations(self):
        self.decisionSplitting.update({6: [False, False, True, True, True, True, False, False, False, False]})
        self.decisionSplitting.update({4: [False, False, False, False, False, False, False, False, False, False]})
        self.decisionSplitting.update({3: [False, False, False, True, True, True, True, False, False, False]})
        self.decisionSplitting.update({2: [False, False, False, True, True, True, True, False, False, False]})
        
    def countingSplittingDeviations(self, count, decksRemaining):
        decisionSplitcopy = self.decisionSplitting.copy()
        
        if count.getTrueCount(decksRemaining) >= 6:
            decisionSplitcopy.update({10: [False, False, False, True, True, True, False, False, False, False]})
        elif count.getTrueCount(decksRemaining) >= 5:
            decisionSplitcopy.update({10: [False, False, False, False, True, True, False, False, False, False]})
        elif count.getTrueCount(decksRemaining) >= 4:
            decisionSplitcopy.update({10: [False, False, False, False, False, True, False, False, False, False]})
            
        return decisionSplitcopy
    
    def countingHardDeviation(self, count, decksRemaining):
        decisionHardcopy = self.decisionHardTotal.copy()
        
        if count.getTrueCount(decksRemaining) >= 4:
            decisionHardcopy.update({16: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'S', 'S']})
            decisionHardcopy.update({15: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S']})
            decisionHardcopy.update({12: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H']})
            decisionHardcopy.update({11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']})
            decisionHardcopy.update({10: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']})
            decisionHardcopy.update({9: ['H', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H']})
            decisionHardcopy.update({8: ['H', 'H', 'H', 'H', 'H', 'D', 'H', 'H', 'H', 'H']})
        elif count.getTrueCount(decksRemaining) >= 3:
            decisionHardcopy.update({16: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S']})
            decisionHardcopy.update({12: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H']})
            decisionHardcopy.update({11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']})
            decisionHardcopy.update({9: ['H', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H']})
            decisionHardcopy.update({8: ['H', 'H', 'H', 'H', 'H', 'D', 'H', 'H', 'H', 'H']})
        elif count.getTrueCount(decksRemaining) >= 2:
            decisionHardcopy.update({16: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S']})
            decisionHardcopy.update({12: ['H', 'H', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H']})
            decisionHardcopy.update({11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']})
            decisionHardcopy.update({9: ['H', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H']})
            decisionHardcopy.update({8: ['H', 'H', 'H', 'H', 'H', 'D', 'H', 'H', 'H', 'H']})
        elif count.getTrueCount(decksRemaining) >= 1:
            decisionHardcopy.update({16: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S']})
            decisionHardcopy.update({11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']})
            decisionHardcopy.update({9: ['H', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H']})
        elif count.runningCount > 0:
            decisionHardcopy.update({16: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S']})
        elif count.getTrueCount(decksRemaining) <= -1:
            decisionHardcopy.update({13: ['H', 'H', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H']})
            decisionHardcopy.update({12: ['H', 'H', 'H', 'H', 'S', 'S', 'H', 'H', 'H', 'H']})
        elif count.runningCount < 0:
            decisionHardcopy.update({12: ['H', 'H', 'H', 'H', 'S', 'S', 'H', 'H', 'H', 'H']})
            
        return decisionHardcopy
    
    def countingSurrenderDeviation(self, count, decksRemaining):
        decisionSurrendercopy = self.decisionSurrender.copy()
        
        if count.getTrueCount(decksRemaining) >= 4:
            decisionSurrendercopy.update({16: [True, False, False, False, False, False, False, True, True, True]})
            decisionSurrendercopy.update({15: [True, False, False, False, False, False, False, False, True, True]})
        elif count.getTrueCount(decksRemaining) >= 2:
            decisionSurrendercopy.update({15: [True, False, False, False, False, False, False, False, True, True]})
        elif count.getTrueCount(decksRemaining) < -1:
            decisionSurrendercopy.update({16: [True, False, False, False, False, False, False, False, False, True]})
            decisionSurrendercopy.update({15: [False, False, False, False, False, False, False, False, False, False]})
        elif count.runningCount < 0:
            decisionSurrendercopy.update({15: [False, False, False, False, False, False, False, False, False, False]})
            
        return decisionSurrendercopy
    
    def hardTotalAction(self, hand, dealerUpCard, softAceCount, count, decksRemaining):
        if random.randrange(0,1) > self.strategyAccuracy:
            return random.choice(['H', 'D', 'S'])
        handValue = hand.getHandValue(softAceCount)
        
        if dealerUpCard.getRank() > 10:
            upCard = 10
        else:
            upCard = dealerUpCard.getRank()
            
        if handValue <= 8:
            return 'H'
        if handValue >= 17:
            return 'S'
        
        if self.isCounting:
            decisionHardTotal = self.countingHardDeviation(count, decksRemaining)
            action = decisionHardTotal.get(handValue)[upCard - 1]
        else:
            action = self.decisionHardTotal.get(handValue)[upCard - 1]
        if action == 'D' and len(hand.cards) > 2:
            return 'H'
        else:
            return action
    
    def softTotalAction(self, hand, dealerUpCard, softAceCount, count):
        if random.randrange(0,1) > self.strategyAccuracy:
            return random.choice(['H', 'D', 'S'])
        handValue = hand.getHandValue(softAceCount)
        
        if dealerUpCard.getRank() > 10:
            upCard = 10
        else:
            upCard = dealerUpCard.getRank()
            
        return self.decisionSoftTotal.get(handValue)[upCard - 1]
    
    def shouldSplit(self, hand, dealerUpCard, count, decksRemaining):
        pairValue = round(hand.getSoftTotal() / 2)
        
        if dealerUpCard.getRank() > 10:
            upCard = 10
        else:
            upCard = dealerUpCard.getRank()
            
        if pairValue == 11:
            pairValue = 1
            
        if self.isCounting:
            decisionSplitting = self.countingSplittingDeviations(count, decksRemaining)
            return decisionSplitting.get(pairValue)[upCard - 1]
        else:
            return self.decisionSplitting.get(pairValue)[upCard - 1]
    
    def shouldSurrender(self, hand, dealerUpCard, count, decksRemaining):
        handValue = hand.getSoftTotal()
        
        if dealerUpCard.getRank() > 10:
            upCard = 10
        else:
            upCard = dealerUpCard.getRank()
            
        if self.HouseRules.LSoffered:
            if handValue in [15,16]:
                if self.isCounting:
                    if hand.isPair():
                        return False
                    decisionSurrender = self.countingSurrenderDeviation(count, decksRemaining)
                    return decisionSurrender.get(handValue)[upCard - 1]
                else:
                    if hand.isPair():
                        return False
                    return self.decisionSurrender.get(handValue)[upCard - 1]
        return False
    
    def takeInsurance(self, count, decksRemaining):
        if self.isCounting:
            if count.getTrueCount(decksRemaining) >= 3:
                return True
        return False
    
    
class BasicStrategyH17(StrategyFormat):
    def __init__(self, isCounting, strategyAccuracy, count, HouseRules):
        self.isCounting = isCounting
        self.strategyAccuracy = strategyAccuracy
        self.HouseRules = HouseRules
        
        self.decisionSplitting = {
            #     A     2     3     4     5     6     7     8     9     10
            1: [True, True, True, True, True, True, True, True, True, True],
            10: [False, False, False, False, False, False, False, False, False, False],
            9: [False, True, True, True, True, True, False, True, True, False],
            8: [True, True, True, True, True, True, True, True, True, True],
            7: [False, True, True, True, True, True, True, False, False, False],
            6: [False, True, True, True, True, True, False, False, False, False],
            5: [False, False, False, False, False, False, False, False, False, False],
            4: [False, False, False, False, True, True, False, False, False, False],
            3: [False, True, True, True, True, True, True, False, False, False],
            2: [False, True, True, True, True, True, True, False, False, False]
        }
        
        self.decisionSoftTotal = {
            #     A    2    3    4    5    6    7    8    9    10
            21: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            19: ['S', 'S', 'S', 'S', 'S', 'D', 'S', 'S', 'S', 'S'],
            18: ['H', 'D', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H'],
            17: ['H', 'H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],
            16: ['H', 'H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],
            15: ['H', 'H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],
            14: ['H', 'H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H'],
            13: ['H', 'H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H'],
            11: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
        }
        
        self.decisionHardTotal = {
            #     A    2    3    4    5    6    7    8    9    10
            17: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            16: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],
            15: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],
            14: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],
            13: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],
            12: ['H', 'H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],
            11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],
            10: ['H', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'],
            9: ['H', 'H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],
            8: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
        }
        
        self.decisionSurrender = {
            17: [True, False, False, False, False, False, False, False, False, False],
            16: [True, False, False, False, False, False, False, False, True, True],
            15: [True, False, False, False, False, False, False, False, False, True],
            88: [True, False, False, False, False, False, False, False, False, False]
        }
        
        if HouseRules.DASoffered == False:
            self.DASdeviations()
    
    def DASdeviations(self):
        self.decisionSplitting.update({6: [False, False, True, True, True, True, False, False, False, False]})
        self.decisionSplitting.update({4: [False, False, False, False, False, False, False, False, False, False]})
        self.decisionSplitting.update({3: [False, False, False, True, True, True, True, False, False, False]})
        self.decisionSplitting.update({2: [False, False, False, True, True, True, True, False, False, False]})
     
    def countingSplittingDeviations(self, count, decksRemaining):
        decisionSplitcopy = self.decisionSplitting.copy()
        
        if count.getTrueCount(decksRemaining) >= 6:
            decisionSplitcopy.update({10: [False, False, False, True, True, True, False, False, False, False]})
        elif count.getTrueCount(decksRemaining) >= 5:
            decisionSplitcopy.update({10: [False, False, False, False, True, True, False, False, False, False]})
        elif count.getTrueCount(decksRemaining) >= 4:
            decisionSplitcopy.update({10: [False, False, False, False, False, True, False, False, False, False]})
            
        return decisionSplitcopy
    
    def countingHardDeviation(self, count, decksRemaining):
        decisionHardcopy = self.decisionHardTotal.copy()
        
        if count.getTrueCount(decksRemaining) >= 5:
            decisionHardcopy.update({16: ['S', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'S', 'S']})
            decisionHardcopy.update({15: ['S', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S']})
            decisionHardcopy.update({12: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H']})
            decisionHardcopy.update({10: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']})
            decisionHardcopy.update({9: ['H', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H']})
            decisionHardcopy.update({8: ['H', 'H', 'H', 'H', 'H', 'D', 'H', 'H', 'H', 'H']})
        elif count.getTrueCount(decksRemaining) >= 4:
            decisionHardcopy.update({16: ['S', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'S', 'S']})
            decisionHardcopy.update({15: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S']})
            decisionHardcopy.update({12: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H']})
            decisionHardcopy.update({10: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']})
            decisionHardcopy.update({9: ['H', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H']})
            decisionHardcopy.update({8: ['H', 'H', 'H', 'H', 'H', 'D', 'H', 'H', 'H', 'H']})
        elif count.getTrueCount(decksRemaining) >= 3:
            decisionHardcopy.update({16: ['S', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S']})
            decisionHardcopy.update({12: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H']})
            decisionHardcopy.update({10: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H']})
            decisionHardcopy.update({9: ['H', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H']})
            decisionHardcopy.update({8: ['H', 'H', 'H', 'H', 'H', 'D', 'H', 'H', 'H', 'H']})
        elif count.getTrueCount(decksRemaining) >= 2:
            decisionHardcopy.update({16: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S']})
            decisionHardcopy.update({12: ['H', 'H', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H']})
            decisionHardcopy.update({9: ['H', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H']})
            decisionHardcopy.update({8: ['H', 'H', 'H', 'H', 'H', 'D', 'H', 'H', 'H', 'H']})
        elif count.getTrueCount(decksRemaining) >= 1:
            decisionHardcopy.update({16: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S']})
            decisionHardcopy.update({9: ['H', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H']})
        elif count.runningCount > 0:
            decisionHardcopy.update({16: ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S']})
        elif count.getTrueCount(decksRemaining) <= -1:
            decisionHardcopy.update({13: ['H', 'H', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H']})
            decisionHardcopy.update({12: ['H', 'H', 'H', 'H', 'S', 'S', 'H', 'H', 'H', 'H']})
        elif count.runningCount < 0:
            decisionHardcopy.update({12: ['H', 'H', 'H', 'H', 'S', 'S', 'H', 'H', 'H', 'H']})
            
        return decisionHardcopy
    
    def countingSurrenderDeviation(self, count, decksRemaining):
        decisionSurrendercopy = self.decisionSurrender.copy()
        
        if count.getTrueCount(decksRemaining) >= 4:
            decisionSurrendercopy.update({16: [True, False, False, False, False, False, False, True, True, True]})
            decisionSurrendercopy.update({15: [True, False, False, False, False, False, False, False, True, True]})
        elif count.getTrueCount(decksRemaining) >= 2:
            decisionSurrendercopy.update({15: [True, False, False, False, False, False, False, False, True, True]})
        elif count.getTrueCount(decksRemaining) > -1:
            decisionSurrendercopy.update({15: [True, False, False, False, False, False, False, False, False, True]})
        elif count.getTrueCount(decksRemaining) == -1:
            decisionSurrendercopy.update({16: [True, False, False, False, False, False, False, False, False, True]})
            decisionSurrendercopy.update({15: [True, False, False, False, False, False, False, False, False, False]})
        elif count.getTrueCount(decksRemaining) < -1:
            decisionSurrendercopy.update({16: [True, False, False, False, False, False, False, False, False, True]})
            decisionSurrendercopy.update({15: [False, False, False, False, False, False, False, False, False, False]})
        elif count.runningCount < 0:
            decisionSurrendercopy.update({15: [True, False, False, False, False, False, False, False, False, False]})
            
        return decisionSurrendercopy
   
    def hardTotalAction(self, hand, dealerUpCard, softAceCount, count, decksRemaining):
        if random.randrange(0,1) > self.strategyAccuracy:
            return random.choice(['H', 'D', 'S'])
        handValue = hand.getHandValue(softAceCount)
        
        if dealerUpCard.getRank() > 10:
            upCard = 10
        else:
            upCard = dealerUpCard.getRank()
            
        if handValue <= 8:
            return 'H'
        if handValue >= 17:
            return 'S'
        
        if self.isCounting:
            decisionHardTotal = self.countingHardDeviation(count, decksRemaining)
            action = decisionHardTotal.get(handValue)[upCard - 1]
        else:
            action = self.decisionHardTotal.get(handValue)[upCard - 1]
        if action == 'D' and len(hand.cards) > 2:
            return 'H'
        else:
            return action
        
    
    def softTotalAction(self, hand, dealerUpCard, softAceCount, count):
        if random.randrange(0,1) > self.strategyAccuracy:
            return random.choice(['H', 'D', 'S'])
        handValue = hand.getHandValue(softAceCount)
        
        if dealerUpCard.getRank() > 10:
            upCard = 10
        else:
            upCard = dealerUpCard.getRank()
            
        return self.decisionSoftTotal.get(handValue)[upCard - 1]
    
    def shouldSplit(self, hand, dealerUpCard, count, decksRemaining):
        pairValue = round(hand.getSoftTotal() / 2)
        
        if dealerUpCard.getRank() > 10:
            upCard = 10
        else:
            upCard = dealerUpCard.getRank()
            
        if pairValue == 11:
            pairValue = 1
            
        if self.isCounting:
            decisionSplitting = self.countingSplittingDeviations(count, decksRemaining)
            return decisionSplitting.get(pairValue)[upCard - 1]
        else:
            return self.decisionSplitting.get(pairValue)[upCard - 1]
    
    def shouldSurrender(self, hand, dealerUpCard, count, decksRemaining):
        handValue = hand.getSoftTotal()
        
        if dealerUpCard.getRank() > 10:
            upCard = 10
        else:
            upCard = dealerUpCard.getRank()
          
        if self.HouseRules.LSoffered:
            if handValue in [15,16,17]:
                if self.isCounting:
                    if hand.isPair():
                        return False
                    decisionSurrender = self.countingSurrenderDeviation(count, decksRemaining)
                    return decisionSurrender.get(handValue)[upCard - 1]
                else:
                    if hand.isPair():
                        return self.decisionSurrender.get(88)[upCard - 1]
                    return self.decisionSurrender.get(handValue)[upCard - 1]
        return False
    
    def takeInsurance(self, count, decksRemaining):
        if self.isCounting:
            if count.getTrueCount(decksRemaining) >= 3:
                return True
        return False