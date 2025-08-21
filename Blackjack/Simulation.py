from Card import Card, Suit, CardValue
from Deck import Deck
from Hand import Hand
from Player import Player
from Dealer import Dealer
from Count import HiLoCount
from Strategy import BasicStrategyS17, BasicStrategyH17, CasinoStrategy, RandomStrategy, NoBustStrategy
from Betting import FlatSpread, RandomSpread, Spread1_6, Spread1_8, Spread1_12, Spread1_25_WongOut
from HouseRules import HouseRules
from Plotting import bankrollPlot
import statistics

class BlackjackSimulation:
    def __init__(self, players, count, HouseRules):
        self.HouseRules = HouseRules
        self.dealer = Dealer(HouseRules.numDecks, HouseRules.penetration, 
                             CasinoStrategy(isCounting = False, strategyAccuracy = 1, 
                                            count = count, HouseRules=HouseRules))
        self.players = players
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
        player.totalWagered += betSize

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
        player.totalWagered += hand.betSize / 2
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
        player.rollingBankroll += hand.betSize * self.HouseRules.NBJpayout
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
                    player.rollingBankroll += 0
                else:
                    player.rollingBankroll -= hand.betSize
                    self.stats['dealer_wins'] += 1

    def handleSplit(self, player, hand, dealerUpCard, count, decksRemaining):
        if player.strategy.shouldSplit(hand, dealerUpCard, count, decksRemaining):
            splitHand = player.splitPair(hand)
            player.totalWagered += splitHand.betSize
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
        player.rollingBankroll -= hand.betSize
        # print(hand.printHand())
        
    def handleInsurance(self, players, count, decksRemaining):
        for player in players:
            for hand in player.hands:
                if player.strategy.takeInsurance(count, decksRemaining):
                    hand.insureHand()
                    player.totalWagered += hand.insuranceBet
                    self.stats['insurance_taken'] += 1
                    
    def handleSurrender(self, player, hand):
        player.clearHand(hand)
        self.stats['dealer_wins'] += 1
        self.stats['surrender'] += 1
        player.rollingBankroll -= hand.betSize * 0.5
        
    def playerTurn(self, player, count):
        initialHand = player.getInitialHand()
        dealerUpCard = self.dealer.upCard

        if initialHand.isBlackjack():
            self.handlePlayerBlackjack(player, initialHand)
            
        if (player.strategy.shouldSurrender(initialHand, dealerUpCard, count, 
                                           self.dealer.getDecksRemaining()) and 
                                            initialHand.getAceCount() == 0):
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
                        splitHand = self.handleSplit(player, handInPlay, dealerUpCard, 
                                                     count, decksRemaining)
                        if splitHand is not None:
                            self.stats['split_hands'] += 1
                            if splitHand.cards[0].getRank() == 1:
                                self.handleSplitAces(handInPlay, splitHand, count)
                                break
                            else:
                                self.actionHit(handInPlay, count)
                                self.actionHit(splitHand, count)
                    
                    if softAceCount < handInPlay.getAceCount():
                        handInPlay.action = player.strategy.softTotalAction(handInPlay, 
                                                                            dealerUpCard, 
                                                                            softAceCount, 
                                                                            count)
                    else:
                        handInPlay.action = player.strategy.hardTotalAction(handInPlay, 
                                                                            dealerUpCard, 
                                                                            softAceCount, 
                                                                            count, 
                                                                            decksRemaining)
                        
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
                action = self.dealer.strategy.softTotalAction(dealerHand, 
                                                              dealerUpCard, 
                                                              softAceCount, 
                                                              count)
            else:
                action = self.dealer.strategy.hardTotalAction(dealerHand, 
                                                              dealerUpCard, 
                                                              softAceCount, 
                                                              count)
            
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
                        player.rollingBankroll += hand.betSize
                        if hand.isDoubled:
                            self.stats['double_wins'] += 1
                    elif result == "dealer":
                        self.stats['dealer_wins'] += 1
                        player.rollingBankroll -= hand.betSize
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

class MonteCarloSimulation:
    def __init__(self, houserules, playerConfigs):
        self.HouseRules = houserules
        self.plotting = bankrollPlot()
        self.playerConfigs = playerConfigs  
        
    def create_players(self, count):
        players = []
        for config in self.playerConfigs:
            player = Player(
                initialBankroll=config['initialBankroll'],
                strategy=config['strategy_class'](
                    isCounting=config['isCounting'],
                    strategyAccuracy=config['strategyAccuracy'],
                    count=count,
                    HouseRules=self.HouseRules
                ),
                betting=config['betting']()
            )
            players.append(player)
        return players
        
    def RunSimulations(self, numTrials, numHands, isTrialsVerbose, count):
        finalBankroll = []
        handsPlayed = []
        houseEdge = []
        
        for k in range(numTrials):
            # Create fresh players for each trial
            fresh_players = self.create_players(count)
            
            game = BlackjackSimulation(players=fresh_players, count=count, 
                                       HouseRules=self.HouseRules)
            game.dealer.shuffleDeck()
            
            for i in range(numHands): 
                if game.dealer.penetrationReached():
                    game.dealer.shuffleDeck()
                    count.resetCount()
                
                game.playSingleGame(count)
                game.gameOver(count)
                
                game.stats['games_played'] += 1
                self.plotting.recordHandBankroll(game.players[0])

            total_hands = game.stats['games_played'] + game.stats['split_hands']
            self.plotting.recordRoundBankroll()
            
            if isTrialsVerbose:
                print("\n" + "="*50)
                print("BLACKJACK GAME RESULTS")
                print("="*50)
                print(f"Total Hands Played: {total_hands}")
                print(f"Splits: {game.stats['split_hands']}")
                print(f"Doubles: {game.stats['doubles']}")
                print(f"Double Wins: {game.stats['double_wins']}")
                print(f"Double Losses: {game.stats['double_loss']}")
                print(f"Insurance Taken: {game.stats['insurance_taken']}")
                print(f"Surrender: {game.stats['surrender']}")
                print(f"Player Wins: {game.stats['player_wins']} ({game.stats['player_wins']/total_hands*100:.1f}%)")
                print(f"Dealer Wins: {game.stats['dealer_wins']} ({game.stats['dealer_wins']/total_hands*100:.1f}%)")
                print(f"Pushes: {game.stats['pushes']} ({game.stats['pushes']/total_hands*100:.1f}%)")
                print(f"Player Blackjacks: {game.stats['blackjacks']} ({game.stats['blackjacks']/total_hands*100:.1f}%)")
                for player in game.players:
                    print(f"Final Bankroll: {player.rollingBankroll}")
                    print(f"House Edge: {((player.rollingBankroll-50000)/(player.totalWagered))*100:.2f}%")
                print("="*50)
        
            finalBankroll.append(game.players[0].rollingBankroll)
            handsPlayed.append(total_hands)
            houseEdge.append(((game.players[0].rollingBankroll-50000) / game.players[0].totalWagered) * 100)
            meanhouseEdge = statistics.mean(houseEdge)
    
        if len(finalBankroll) > 1:
            meanHands = statistics.mean(handsPlayed)
            meanBR = statistics.mean(finalBankroll)
            median = statistics.median(finalBankroll)
            stdev = statistics.stdev(finalBankroll)
            meanhouseEdge = statistics.mean(houseEdge)
            houseEdge_stdev = statistics.stdev(houseEdge)
            
            print("\n" + "="*50)
            print("MONTE CARLO SIMULATION RESULTS")
            print("="*50)
            print(f"Total Hands Played: {meanHands: .0f}")
            print(f"Mean Final Bankroll: ${meanBR: .2f}")
            print(f"Median Final Bankroll: ${median: .2f}")
            print(f"Final Bankroll Std. Dev.: ${stdev: .2f}")
            print(f"Mean Player Edge: {meanhouseEdge: .2f}%")
            print(f"Edge Std. Dev.: {houseEdge_stdev: .2f}%")
        
            self.plotting.plotMCResults(meanhouseEdge)