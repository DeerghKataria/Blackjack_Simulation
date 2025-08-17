import random

class FlatSpread:
    def __init__(self):
        self.name = 'Flat Spread'
        
    def getBetSize(self, trueCount, tableMin):
        return tableMin
    
    
class RandomSpread:
    def __init__(self):
        self.name = 'Random Spread'
        
    def getBetSize(self, trueCount, tableMin):
        return random.choice([tableMin, tableMin*2, tableMin*3, tableMin*4])
    

class Spread1_6:
    def __init__(self):
        self.name = '1-6 Spread'
        
    def getBetSize(self, trueCount, tableMin):
        if trueCount < 0: return tableMin
        if trueCount > 5: return tableMin * 6
        
        betSpread = {
            0: tableMin,
            1: tableMin * 2,
            2: tableMin * 3,
            3: tableMin * 4,
            4: tableMin * 5,
            5: tableMin * 6
        }
        
        return betSpread.get(trueCount)
    
class Spread1_8:
    def __init__(self):
        self.name = '1-8 Spread'
        
    def getBetSize(self, trueCount, tableMin):
        if trueCount < 0: return tableMin
        if trueCount > 5: return tableMin * 8
        
        betSpread = {
            0: tableMin,
            1: tableMin * 2,
            2: tableMin * 3,
            3: tableMin * 4,
            4: tableMin * 6,
            5: tableMin * 8
        }
        
        return betSpread.get(trueCount)
    
class Spread1_12:
    def __init__(self):
        self.name = '1-8 Spread'
        
    def getBetSize(self, trueCount, tableMin):
        if trueCount < 0: return tableMin
        if trueCount > 5: return tableMin * 12
        
        betSpread = {
            0: tableMin,
            1: tableMin * 2,
            2: tableMin * 4,
            3: tableMin * 6,
            4: tableMin * 10,
            5: tableMin * 12
        }
        
        return betSpread.get(trueCount)