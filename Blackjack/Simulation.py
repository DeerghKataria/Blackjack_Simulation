from Card import Card, Suit, CardValue
from Deck import Deck
from Hand import Hand
from Player import Player
from Dealer import Dealer
from Count import HiLoCount
from Strategy import BasicStrategyS17, BasicStrategyH17, CasinoStrategy, RandomStrategy
from Betting import FlatSpread, RandomSpread, Spread1_6, Spread1_8, Spread1_12
from HouseRules import HouseRules
from Plotting import bankrollPlot

class BlackjackSimulation:
    def __init__(self, count, HouseRules):
        self.HouseRules = HouseRules
        self.dealer = Dealer(HouseRules.numDecks, HouseRules.penetration, CasinoStrategy(isCounting = False, strategyAccuracy = 1, count = count, HouseRules=HouseRules))
        self.players = [Player(initialBankroll=10000, strategy = BasicStrategyS17(isCounting = False, strategyAccuracy = 1, count = count, HouseRules=HouseRules), betting = RandomSpread())]
        self.stats = {
            'games_played': 0,
            'player_wins': 0,
            'dealer_wins': 0,
            'pushes': 0,
            'blackjacks': 0,
            'split_hands': 0,
            'doubles': 0,
            'double_wins': 0,
            'double_loss': 0,
            'insurance_taken': 0,
            'surrender': 0
        }

    def dealInitialCards(self, player, count, betSize = None):
        if betSize == None:
            betSize = self.HouseRules.minBet
        # Clear Player Cards
        player.hands = []

        # Deal Player Cards and set bet size
        cards = [self.dealer.dealCard(), self.dealer.dealCard()]
        for card in cards:
            count.updateCount(card)
        hand = Hand(cards, betSize=betSize)
        player.updateHand(hand)

    def dealDealerCards(self, count):
        dealerCards = [self.dealer.dealCard(), self.dealer.dealCard()]
        dealerHand = Hand(dealerCards, 0)
        self.dealer.updateHand(dealerHand)
        upCard = dealerCards[0]
        self.dealer.setUpCard(upCard)
        count.updateCount(upCard)

    def actionHit(self, hand, count):
        hitCard = self.dealer.dealCard()
        count.updateCount(hitCard)
        hand.cards.append(hitCard)

    def actionDouble(self, player, hand, softAceCount, count):
        hand.doubleDown()
        self.actionHit(hand, count)
        self.stats['doubles'] += 1
        newSoftAceCount = softAceCount
        while hand.isBust(newSoftAceCount) and newSoftAceCount < hand.getAceCount():
            newSoftAceCount += 1
        if hand.isBust(newSoftAceCount):
            self.handleBust(player, hand)
        else:
            hand.finalValue = hand.getHandValue(newSoftAceCount)
        

    def handlePlayerBlackjack(self, player, hand):
        player.bankroll += hand.betSize * self.HouseRules.NBJpayout
        self.dealer.discardPlayerHand(hand)
        player.clearHand(hand)
        self.stats['blackjacks'] += 1
        self.stats['player_wins'] += 1

    def handleDealerBlackjack(self, players, count):
        for player in players:
            for hand in player.hands:
                if hand.isBlackjack():
                    self.stats['pushes'] += 1
                elif hand.isInsured:
                    player.bankroll += 0
                else:
                    player.bankroll -= hand.betSize
                    self.stats['dealer_wins'] += 1

    def handleSplit(self, player, hand, dealerUpCard, count, decksRemaining):
        if player.strategy.shouldSplit(hand, dealerUpCard, count, decksRemaining):
            splitHand = player.splitPair(hand)
            hand.isSplit = True
            splitHand.isSplit = True
            return splitHand
        return None
    
    def handleSplitAces(self, handInPlay, splitHand, count):
        self.actionHit(handInPlay, count)
        self.actionHit(splitHand, count)
        handInPlay.action = 'S'
        newSoftAceCount = 0
        if handInPlay.isBust(newSoftAceCount):
            if newSoftAceCount < handInPlay.getAceCount():
                newSoftAceCount += 1
        handInPlay.finalValue = handInPlay.getHandValue(newSoftAceCount)
        splitHand.action = 'S'
        newSoftAceCount = 0
        if splitHand.isBust(newSoftAceCount):
            if newSoftAceCount < splitHand.getAceCount():
                newSoftAceCount += 1
        splitHand.finalValue = splitHand.getHandValue(newSoftAceCount)
    
    def handleBust(self, player, hand):
        self.dealer.discardPlayerHand(hand)
        player.clearHand(hand)
        self.stats['dealer_wins'] += 1
        player.bankroll -= hand.betSize
        # print(hand.printHand())
        
    def handleInsurance(self, players, count, decksRemaining):
        for player in players:
            for hand in player.hands:
                if player.strategy.takeInsurance(count, decksRemaining):
                    hand.insureHand()
                    self.stats['insurance_taken'] += 1
                    
    def handleSurrender(self, player, hand):
        player.clearHand(hand)
        self.stats['dealer_wins'] += 1
        self.stats['surrender'] += 1
        player.bankroll -= hand.betSize * 0.5
        
    def playerTurn(self, player, count):
        initialHand = player.getInitialHand()
        dealerUpCard = self.dealer.upCard

        if initialHand.isBlackjack():
            self.handlePlayerBlackjack(player, initialHand)
            
        if player.strategy.shouldSurrender(initialHand, dealerUpCard, count, self.dealer.getDecksRemaining()) and initialHand.getAceCount() == 0:
            self.handleSurrender(player, initialHand)
        
        else:
            i=0
            while i < len(player.hands):
                handInPlay = player.hands[i]
                softAceCount = 0
                decksRemaining = self.dealer.getDecksRemaining()

                while handInPlay.action != 'S':
                    if handInPlay.isBust(softAceCount):
                        if softAceCount < handInPlay.getAceCount():
                            softAceCount += 1
                        else:
                            self.handleBust(player, handInPlay)
                            break
                            
                    if handInPlay.isPair():
                        splitHand = self.handleSplit(player, handInPlay, dealerUpCard, count, decksRemaining)
                        if splitHand is not None:
                            self.stats['split_hands'] += 1
                            if splitHand.cards[0].getRank() == 1:
                                self.handleSplitAces(handInPlay, splitHand, count)
                                break
                            else:
                                self.actionHit(handInPlay, count)
                                self.actionHit(splitHand, count)
                    
                    if softAceCount < handInPlay.getAceCount():
                        handInPlay.action = player.strategy.softTotalAction(handInPlay, dealerUpCard, softAceCount, count)
                    else:
                        handInPlay.action = player.strategy.hardTotalAction(handInPlay, dealerUpCard, softAceCount, count, decksRemaining)
                        
                    if handInPlay.action == 'H':
                        self.actionHit(handInPlay, count)
                    elif handInPlay.action == 'D':
                        self.actionDouble(player, handInPlay, softAceCount, count)
                        break
                    elif handInPlay.action == 'S':
                        handInPlay.finalValue = handInPlay.getHandValue(softAceCount)
                        
                if handInPlay in player.hands:
                    i += 1

    def dealerTurn(self, count):
        dealerHand = self.dealer.hand
        action = None
        softAceCount = 0
        dealerUpCard = None

        while action != 'S':
            if dealerHand.isBust(softAceCount):
                if softAceCount < dealerHand.getAceCount():
                    softAceCount += 1
                else:
                    break

            if softAceCount < dealerHand.getAceCount():
                action = self.dealer.strategy.softTotalAction(dealerHand, dealerUpCard, softAceCount, count)
            else:
                action = self.dealer.strategy.hardTotalAction(dealerHand, dealerUpCard, softAceCount, count)
            
            if action == 'H':
                self.actionHit(dealerHand, count)
            elif action == 'S':
                dealerHand.finalValue = dealerHand.getHandValue(softAceCount)
                break

    def determineWinner(self, hand):
        playerValue = hand.finalValue
        dealerValue = self.dealer.hand.finalValue
        
        if playerValue > dealerValue:
            return 'player'
        
        elif playerValue < dealerValue:
            return 'dealer'
        
        else:
            return 'push'
        
    def playSingleGame(self, count):

        # Determine Bet Size and deal player cards
        decksRemaining = self.dealer.getDecksRemaining()
        trueCount = count.getTrueCount(decksRemaining)
        tableMin = self.HouseRules.minBet
        for player in self.players:
            betSize = player.betting.getBetSize(trueCount, tableMin)
            self.dealInitialCards(player, count, betSize=betSize)
        
        # Deal Dealer Cards
        self.dealDealerCards(count)
        
        # Check if Insurance should be offered
        if self.dealer.offerInsurance():
            self.handleInsurance(self.players, count, self.dealer.getDecksRemaining())

        # Check for Dealer Blackjack
        if self.dealer.hand.isBlackjack():
            self.handleDealerBlackjack(self.players, count)

        else:
            # Player Turn
            for player in self.players:
                self.playerTurn(player, count)
                        
    
            # Check if player isn't bust
            anyPlayerAlive = False
            for player in self.players:
                if len(player.hands) > 0:
                    anyPlayerAlive = True
                    break
    
            # Dealer's Turn
            if anyPlayerAlive:
                self.dealerTurn(count)
    
            # Determine Winner
            for player in self.players:
                for hand in player.hands:
                    # print(hand.printHand())
                    # print(hand.finalValue)
                    # print('\n')
                    # print(self.dealer.hand.printHand())
                    # print(self.dealer.hand.finalValue)
                    result = self.determineWinner(hand)
                    # print(result)
                    # print('\n\n')
                    if result == "player": 
                        self.stats['player_wins'] += 1
                        player.bankroll += hand.betSize
                        if hand.isDoubled:
                            self.stats['double_wins'] += 1
                    elif result == "dealer":
                        self.stats['dealer_wins'] += 1
                        player.bankroll -= hand.betSize
                        if hand.isDoubled:
                            self.stats['double_loss'] += 1
                    else:  # push
                        self.stats['pushes'] += 1

    def gameOver(self, count):
        # Update Count with Dealer Hidden Card
        count.updateCount(self.dealer.hand.cards[1])

        # Discard Hands
        for player in self.players:
            for hand in player.hands:
                self.dealer.discardPlayerHand(hand)
                player.clearHand(hand)

        self.dealer.discardDealerHand()
        self.dealer.clearHand()

finalBankroll = []
handsPlayed = []
houseEdge = []
plot = bankrollPlot()
HouseRules = HouseRules(standS17 = False, DASoffered = True, 
             LSoffered = True, NBJpayout = 1.5, penetration = 2,
             minBet = 10, numDecks = 6)

for k in range(20000):
    # Set Up Count
    count = HiLoCount()

    sim = BlackjackSimulation(count=count, HouseRules=HouseRules)
    sim.dealer.shuffleDeck()
    for i in range(500): 
        if sim.dealer.penetrationReached():
            sim.dealer.shuffleDeck()
            count.resetCount()
        
        sim.playSingleGame(count)
        sim.gameOver(count)
        
        sim.stats['games_played'] += 1
        plot.recordHandBankroll(sim.players[0])
    
    
    total_hands = sim.stats['games_played'] + sim.stats['split_hands']
    plot.recordRoundBankroll()
    # print("\n" + "="*50)
    # print("BLACKJACK SIMULATION RESULTS")
    # print("="*50)
    # print(f"Total Hands Played: {total_hands}")
    # print(f"Splits: {sim.stats['split_hands']}")
    # print(f"Doubles: {sim.stats['doubles']}")
    # print(f"Double Wins: {sim.stats['double_wins']}")
    # print(f"Double Losses: {sim.stats['double_loss']}")
    # print(f"Insurance Taken: {sim.stats['insurance_taken']}")
    # print(f"Surrender: {sim.stats['surrender']}")
    # print(f"Player Wins: {sim.stats['player_wins']} ({sim.stats['player_wins']/total_hands*100:.1f}%)")
    # print(f"Dealer Wins: {sim.stats['dealer_wins']} ({sim.stats['dealer_wins']/total_hands*100:.1f}%)")
    # print(f"Pushes: {sim.stats['pushes']} ({sim.stats['pushes']/total_hands*100:.1f}%)")
    # print(f"Player Blackjacks: {sim.stats['blackjacks']} ({sim.stats['blackjacks']/total_hands*100:.1f}%)")
    # for player in sim.players:
    #     print(f"Final Bankroll: {player.bankroll}")
    #     print(f"House Edge: {((player.bankroll-10000)/total_hands)*10:.2f}%")
    # print("="*50)
    
    finalBankroll.append(sim.players[0].bankroll)
    handsPlayed.append(total_hands)
    houseEdge.append(((sim.players[0].bankroll-10000) / total_hands) * 10)
    
import statistics
meanHands = statistics.mean(handsPlayed)
meanBR = statistics.mean(finalBankroll)
median = statistics.median(finalBankroll)
stdev = statistics.stdev(finalBankroll)
meanhouseEdge = statistics.mean(houseEdge)
houseEdge_stdev = statistics.stdev(houseEdge)
print(meanHands)
print(meanBR)
print(median)
print(stdev)
print(meanhouseEdge)
print(houseEdge_stdev)

plot.plotMCResults(meanhouseEdge)