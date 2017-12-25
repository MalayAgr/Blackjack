import random


class Player(object):

    def __init__(self, name = None, bet = 0.0, hand = [], total = 0, bankroll = 0):

        self.name = name
        self.bet = bet
        self.hand = hand
        self.total = total
        self.bankroll = bankroll


    def __str__(self):

        return self.name + ", you have set a bet of $" + str(self.bet) + ". Current bankroll: $" + str(self.bankroll) + "."


    def setNameAndBet(self, name, bet, bankroll):

        self.name = name
        self.bet = bet
        self.bankroll = bankroll


    def initializeHand(self, card1, card2):

        self.hand.append(card1)
        self.hand.append(card2)

        print("\nTwo cards dealt.")

        if self.hand[0] in ['K', 'Q', 'J', 10]:

            if self.hand[1] in ['K', 'Q', 'J', 10]:
                self.total = 20
            elif self.hand[1] ==  'A':
                self.total = 21
            else:
                self.total = 10 + self.hand[1]

        elif self.hand[1] in ['K', 'Q', 'J', 10]:

            if self.hand[0] in ['K', 'Q', 'J', 10]:
                self.total = 20
            elif self.hand[0] == 'A':
                self.total = 21
            else:
                self.total = 10 + self.hand[0]

        else:

            if self.hand[0] == 'A' and self.hand[1] == 'A':
                self.total = 13
            elif self.hand[0] == 'A':
                self.total = 11 + self.hand[1]
            elif self.hand[1] == 'A':
                self.total = 11 + self.hand[0]
            else:
                self.total = self.hand[0] + self.hand[1]


    def getTotal(self, card):

        if card not in ['K', 'Q', 'J', 'A']:
            self.total += card
        else:
            if card in ['K', 'Q', 'J']:
                self.total += 10
            else:
                if self.total > 10:
                    self.total += 1
                else:
                    self.total += 11




    def addToBankroll(self, amount, multiplier = 2.0):
        self.bankroll += (amount * multiplier)


    def subtractFromBankroll(self, amount):
        self.bankroll -= amount


    def hit(self, deck):
        card = random.choice(deck.deckState)
        print("\nNew card: %s" %card)
        self.hand.append(card)
        self.getTotal(card)
        deck.deckState.remove(card)


class Dealer(object):

    def __init__(self, faceUpCard = None, faceDownCard = None, hand = [], total = 0):

        self.hand = hand
        self.total = total
        self.faceUpCard = faceUpCard
        self.faceDownCard = faceDownCard


    def initializeHandDealer(self, card1, card2, upCard, downCard):
        self.hand.append(card1)
        self.hand.append(card2)
        self.faceUpCard = upCard
        self.faceDownCard = downCard

        print("\nTwo cards dealt.")

        if self.hand[0] in ['K', 'Q', 'J', 10]:

            if self.hand[1] in ['K', 'Q', 'J', 10]:
                self.total = 20
            elif self.hand[1] ==  'A':
                self.total = 21
            else:
                self.total = 10 + self.hand[1]

        elif self.hand[1] in ['K', 'Q', 'J', 10]:

            if self.hand[0] in ['K', 'Q', 'J', 10]:
                self.total = 20
            elif self.hand[0] == 'A':
                self.total = 21
            else:
                self.total = 10 + self.hand[0]

        else:

            if self.hand[0] == 'A' and self.hand[1] == 'A':
                self.total = 13
            elif self.hand[0] == 'A':
                self.total = 11 + self.hand[1]
            elif self.hand[1] == 'A':
                self.total = 11 + self.hand[0]
            else:
                self.total = self.hand[0] + self.hand[1]


    def getTotal(self):

        for i in range(2, len(self.hand)):
            if self.hand[i] not in ['K', 'Q', 'J', 'A']:
                self.total += self.hand[i]
            else:
                if self.hand[i] in ['K', 'Q', 'J']:
                    self.total += 10
                else:
                    if self.total > 10:
                        self.total += 1
                    else:
                        self.total += 11
        return self.total

    def revealCard(self):
        print("\nDealer's face-down card: %s" %self.faceDownCard)
        print("His total: %s" %self.total)


    def takeCard(self, deck):
        print("\nThe dealer will take a card as his total is not more than 16.")
        card = random.choice(deck.deckState)
        self.hand.append(card)
        print("New card: %s" %card)
        print("New total: %s" %self.getTotal())
        deck.deckState.remove(card)



class Deck(object):

    def __init__(self):

        self.deckState = []

        for i in range(2, 11):
            for j in range(1, 5):
                self.deckState.append(i)

        for i in ['K', 'Q', 'J', 'A']:
            for j in range(1, 5):
                self.deckState.append(i)



def rulesAndRegulations():

    print("\n\nRULES:\nThe objective is to beat the dealer.\n"
          "To beat the dealer, the player should not go over 21 (busting) "
          "and should either outscore the dealer, or have the dealer bust.\n"
          "\nAces are counted as 1 or 11, whichever makes a better hand.\n"
          "Cards from 2 to 9 are counted according to pip value.\n"
          "10 and face cards are counted as 10.\n"
          "The value of a hand is the sum of the point values of individual cards.\n"
          "A blackjack is the highest hand, consisting of an ace and any 10-point card."
          "\n\nAfter the player has bet, the dealer will give two cards to him/her, and two to himself. "
          "One of the dealer's cards will be dealt face-up."
          "\n\nIf the dealer has a ten or an ace showing, he will peek at his "
          "face-down card to see if he has a blackjack."
          " If he does, he will turn it over immediately."
          "\n\nWhen the dealer has a blackjack, all wagers will lose, unless the player also has a blackjack, "
          "which will result in a push."
          "\n\nThe player has the following choices: Stand, Hit, Double and Surrender. "
          "Surrender is valid only for the initial two cards."
          "\n\nWhen the player has played his turn, the dealer will turn over his face-down card. "
          "If he has 16 or less, he will draw another card."
          "\n\nIf the dealer goes over 21, the player will win, provided he hasn't busted as well.\n"
          "If the dealer does not bust, the higher point total will win."
          "\n\nWinning wagers pays even money. Winning player blackjack pays 3 to 2.")



def welcome():

    print("Welcome to BlackJack!")
    print("\nThis will be a single player game against the computer (dealer).")
    print("\nWe'll be playing from a single 52-cards deck.")
    familiarCheck = input("\nDo you want to know the rules and regulations of BlackJack? ")

    if familiarCheck.lower().startswith('y'):
        rulesAndRegulations()



def initializePlayer(player):

    name = input("Enter player name: ")
    while True:
        try:
            bankroll = float(input(name + ", what is your bankroll? $"))
            bet = float(input("Okay, place a bet: $"))
        except:
            print("Please enter a number.")
        else:
            player.setNameAndBet(name, bet, bankroll)
            player.subtractFromBankroll(bet)
            print(player)
            break



def dealTwoCardsToPlayer(player, deckState):
    card1 = random.choice(deckState)
    card2 = random.choice(deckState)
    player.initializeHand(card1, card2)
    print("The cards are: {c1} and {c2}".format(c1 = card1, c2 = card2) +
          "\nYour total is: {total}".format(total = player.total))
    deckState.remove(card1)
    deckState.remove(card2)



def dealTwoCardsToDealer(dealer, deckState):
    card1 = random.choice(deckState)
    card2 = random.choice(deckState)
    dealer.initializeHandDealer(card1, card2, card1, card2) #second card1 and card2 for faceUp and faceDown
    print("Face-up card: {upCard}".format(upCard = card1))
    deckState.remove(card1)
    deckState.remove(card2)



def checkTotal(player, dealer):

    if (player.total == 21 > dealer.total ) or (dealer.total > 21 >= player.total):
        print(player.name + ", has won the round!")
    else:
        print("Dealer won the round.")



def checkDealerBlackjack(dealer, player):

    print("\nThe dealer is peaking at his card (face-up card has a value of 10).")

    if dealer.total == 21 and player.total == 21:

        print("\nThere was a push. The game was a tie.")
        player.addToBankroll(player.bet)
        print("Your bet amount was added to your bankroll.")
        return 1

    elif dealer.total == 21:

        print("\nThe game has ended as the dealer had a {downCard} along with the {upCard}.".format(downCard = dealer.faceDownCard, upCard = dealer.faceUpCard))
        print("You lost $%s." %player.bet)
        print("Current bankroll: $%s" %player.bankroll)
        return 1

    elif player.total < 21 < dealer.total:

        print("\nDealer was busted as his face-down card was {downCard}.".format(downCard = dealer.faceDownCard))
        print("Congratulations! You won $%s!" %player.bet)
        player.addToBankroll(player.bet)
        print("Current bankroll: $%s" %player.bankroll)
        return 1

    elif player.total == 21:
        print("\nCongratulations! You have a BlackJack!")
        print("Profit: $%s" %player.bet*1.5)
        player.addToBankroll(player.bet, 2.5)
        print("Current bankroll: $%s" %player.bankroll)
        return 1

    else:
        print("\nDealer does not have a blackjack.")
        return 0



def playerChoice(player):

    print("\nYour current total: %s" %player.total +
          "\nChoose any one.\n"
          "1. Hit.\n"
          "2. Stand.\n"
          "3. Double")

    while True:
        try:
            choice = int(input("Choice: "))
        except IOError:
            print("Please enter an integer value.")
        else:
            if choice not in [1, 2, 3]:
                print("Please enter 1 or 2.")
            else:
                break
    return choice



def surrenderCheck(player):
    surrenderCheck = input("Ready to proceed or do you want to surrender? "
                           "(Note: you won't be able to surrender after this) ").lower()

    if surrenderCheck.startswith('y') or surrenderCheck.startswith('p'):
        print("\nLet's continue, then!")
        return 0

    else:

        player.addToBankroll(player.bet, 0.5)
        print("\nSo sorry that you surrendered. We've added 50% of your bet to your bankroll.")
        print("Bankroll: $%s" % player.bankroll)
        return 1



def gamePlay(player, deck, dealer):

    noOfTurns = 0
    c = 0
    while player.total < 21 and dealer.total < 21:

        choice = playerChoice(player)

        if choice == 1:

            player.hit(deck)

        elif choice == 2:

            noOfTurns += 1

            if noOfTurns == 1:

                dealer.revealCard()

                if dealer.total <= 16:

                    dealer.takeCard(deck)

            else:
                c = 1
                break

        elif choice == 3:
            pass

        else:
            continue

    if c == 1:
        if 21 > player.total > dealer.total:
            print("\nCongratulations! You won!"
                  "\nProfit: $%s" %(player.bet*2))
            player.addToBankroll(player.bet)

        elif 21 > player.total < dealer.total:
            print("\nThe dealer won as he has a higher total. We're sorry.")
            print("You lost: $%s" %player.bet)

        elif player.total == dealer.total:
            print("\nIt was a tie.")
            player.addToBankroll(player.bet, 1)
            print("Your bet amount was added to your bankroll.")

        print("Current bankroll: $%s" % player.bankroll)

    else:
        if player.total == 21 and dealer.total == 21:

            print("\nThere was push. Your bet has been added to your bankroll.")
            player.addToBankroll(player.bet, 1)


        elif player.total == 21:

            print("\nCongratulations! You won!"
                  "\nProfit: $%s" %(player.bet*2))
            player.addToBankroll(player.bet)

        elif dealer.total == 21:
            print("\nThe dealer has hit 21. You lose. We're sorry.")
            print("You lost: %s" %player.bet)

        elif dealer.total > 21:
            print("\nThe dealer has busted. You won. Congratulations!"
                  "\nProfit: $%s" %(player.bet*2))
            player.addToBankroll(player.bet)

        else:
            print("\nYou have busted! Sorry.\n"
                  "You lost $%s." %player.bet)

        print("Current bankroll: $%s" %player.bankroll)



gameState = True
while gameState:

    welcome()
    if input("\nAre you ready? ").lower().startswith("y"):

        player = Player()
        dealer = Dealer()
        deck = Deck()

        initializePlayer(player)

        print("\nDealer is dealing two cards to %s." %player.name)
        dealTwoCardsToPlayer(player, deck.deckState)

        print("\nNow, the dealer will deal two cards to himself.")
        dealTwoCardsToDealer(dealer, deck.deckState)

        if  player.total <= 21:

            if dealer.faceUpCard in ['A', 'K', 'Q', 'J', 10]:

                if checkDealerBlackjack(dealer, player) != 1:

                    if surrenderCheck(player) != 1:
                        gamePlay(player, deck, dealer)

                    else:
                        break

                else:
                    break

            else:
                print("The dealer does not have a visible 10-point card. It is your turn.")
                gamePlay(player, deck, dealer)

        else:
            print("You were busted. Sorry!"
                  "\nYou lost $%s" %player.bet)

    else:
        break
    if input("\n\nWould you like to play again? ").lower().startswith('y'):
        print("\n"*50)
        gameState = True
    else:
        gameState = False



