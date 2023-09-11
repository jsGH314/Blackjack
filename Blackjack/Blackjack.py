import random

def create_deck():  
    #using list comprehension to create the 52 playable cards
    number = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A", "J", "Q", "K"]
    suits = [u"\u2663", u"\u2660", u"\u2666", u"\u2665"]
    deck = [[x, y] for x in number for y in suits]
    
    return deck

#The Deck class will feature actions that a deck of cards is capable of via a "Dealer" class
#A deck of cards can be dealt, and shuffled 
class Deck:
    def __init__(self, cards):
        self.cards = cards
        
    def __repr__(self):
        return str(self.cards)
    
    def deal_card(self):
        pick = self.cards.pop()
        #test = len(self.cards)
        ##print("Cards Remaining: ", test)
        return pick
    
    #This method is helpful for splits
    #def add_card(self, cards):
     #   self.cards.append(cards)
     #   return self.cards
    
    def shuffle_deck(self):
        random.shuffle(self.cards) 
    
    def new_deck(self):
        self.cards = create_deck()

#Next, is the player class
#Players have a name, an amount of cash, and they will have a hand of cards dealt to them 
#Players can choose how much they bet, if they want to make side bets, hit, stay, split cards, or double down. 
class Player:
    def __init__(self, name, cash = 0, bet = 0):
        self.hand = []
        self.split = []
        self.cash = cash
        self.name = name 
        self.bet = bet
        #self.num_aces = 0
        self.stay = False
        #players can double their original bet, and a hit must be made
        self.double_down = False
        self.can_double = True
        #we have to remember that you typically cannot double down on a split
        self.split_cards = False
        self.can_split = False
        #Any hand with an Ace is considered a 'soft' hand
        self.soft_hand = False
        self.has_blackjack = False
            
    def hit(self, deck):
        self.hand.append(deck.deal_card())
        print(f"{self.name}'s cards: " + str(self.hand))
        
        #self.display_count()
        print("Count: " + str(self.card_total()) + "\n")
    #def is_soft_hand(self):
    #    for card in self.hand:
    #        if card[0] == 'A':
    #            self.soft_hand = True
        
    def card_total(self):
        total = 0
        for card in self.hand:
            #Aces are 1 or 11, any hand with an Ace is considered a 'soft' hand
            if card[0] == 'A':
                total += 11
                self.soft_hand = True
                #self.num_aces += 1
            elif card[0] == 'K':
                total += 10
            elif card[0] == 'Q':
                total += 10    
            elif card[0] == 'J':
                total += 10                
            else:
                total += card[0]
        
        if total > 21:
            if self.soft_hand == True:
                return total - 10
            else:
                return total

        return total
    
    def check_for_blackjack(self):
        if self.card_total() == 21:
            self.has_blackjack = True
            
    
    def display_count(self):
        total = self.card_total()
        print("Soft Hand: ", self.soft_hand)
        if self.soft_hand == True:
            if total < 21:
                print("Count: " + str(total) + " or " + str(total - 10)+ "\n")                
            elif total > 21:
                print("Count: " + str(total - 10) + "\n")
            #elif total == 21:
                #print("Count 21, BLACKJACK!")
                #self.has_blackjack = True
        else:
            print("Count: " + str(total) + "\n")
    
    #def split_cards(self, deck):
       #self.split_cards = True
       # self.can_double = False
       # self.cash -= self.bet
       # self.split.append(self.hand.pop())
       # self.hand.append(deck.deal_card())
       # self.split.append(deck.deal_card())
        
        #self.split.append(self("Split 1: ", deck, self.bet))
        #self.split.append(self("Split 2: ", deck, self.bet))
        #for i in self.split:
            #i.add_card(self.cards.pop(0))
            #i.add_card(deck.deal_card())
            
    
    def show_cards(self):
        for card in self.hand:
          return str(card[0]) + " of " + str(card[1]) 
        
#The Dealer is technically a player in the game. So the Dealer class is a subclass of Player
#A dealer can: Deal cards, Check for win/losses
#The dealer must hit a soft 17
class Dealer(Player):
    
    #The "hole card" is the card that stays face down before the dealer plays their hand, 
    #once it is time for the dealer to play their hand, they reveal their second card
    #hole_card = False

    def __init__(self, name, cash=0):
        super().__init__(name)
        self.hand = []
        self.is_winner = False

    def deal_cards(self, player, deck):
        player.hand.append(deck.deal_card())
        player.hand.append(deck.deal_card())
        self.hand.append(deck.deal_card())
        self.hand.append(deck.deal_card())
        
        #can probably do something to clean this up TODO
        #self.is_soft_hand()
        #player.is_soft_hand() 
        
    #def play_hand(self, deck):
        #self.hole_card = True
        
    def check_for_dealer_blackjack(self):
        if self.card_total() == 21:
            if player.has_blackjack == False:
                print("Dealer has Blackjack!")
                print(f"{player.name} Loses \nCash: {player.cash}")
                self.is_there_a_winner = True
            elif player.has_blackjack == True:
                player.cash += player.bet
                print("Push \n Cash: " + str(player.cash))
                self.is_there_a_winner = True 
                
#Check for winner
    def check_for_win(self, player, dealer):
        if player.has_blackjack == True:
            print("BLACKJACK!")
            print(f"{player.name} wins {player.bet * 1.5}$!")
            player.cash += (player.bet * 2.5)
            print(f"Cash {player.cash}$")
            self.is_there_a_winner = True          
        elif int(player.card_total()) > 21 or int(
                dealer.card_total()) == 21 or int(
                dealer.card_total()) > int(player.card_total()):
            print(f"{player.name} Loses \nCash: {player.cash}")
            self.is_there_a_winner = True
        elif int(dealer.card_total()) > 21 or int(
                player.card_total()) == 21 or int(
                player.card_total()) > int(dealer.card_total()):
            print(f"{player.name} wins {player.bet}$!")
            player.cash += (player.bet * 2)
            print(f"Cash {player.cash}$")
            self.is_there_a_winner = True
        else:
            player.cash += player.bet
            print("Push \n Cash: " + str(player.cash))
            self.is_there_a_winner = True

#Check for bust
    def check_for_lose(self, dealer, player):
        if dealer.has_blackjack == True:
            print(f"{player.name} Loses")
            print(f"Cash {player.cash}$")
            self.is_there_a_winner = True 
        elif int(player.card_total()) > 21:
            print(f"{player.name} Loses")
            print(f"Cash {player.cash}$")
            self.is_there_a_winner = True
        elif int(dealer.card_total()) > 21:
            print(f"{player.name} wins {player.bet}$!")
            player.cash += (player.bet * 2)
            print(f"Cash {player.cash}$")
            self.is_there_a_winner = True
        else:
            pass

    def new_hand(self, player, dealer):
        player.hand = []
        dealer.hand = []

    def new_game(self):
        print("======================================================")
        another_game = input("Play another round?  y/n:  ")
        if another_game == "y":
            deck1.new_deck()
            #new_deck = create_deck()
            #deck1 = Deck(new_deck)
            deck1.shuffle_deck()
            player.soft_hand = False
            dealer1.soft_hand = False
            begin_game()
        else:
            pass
   
        
dealer1 = Dealer("Dealer")
deck1 = Deck(create_deck())
deck1.shuffle_deck()
name = input("Please input your name: ")
player = Player(name, 200)
print("`~*- BLACKJACK -*~`\n")
print(f"\n Welcome {name}!\n")

def begin_game():
    player.stay = False
    dealer1.stay = False
    player.has_blackjack = False
    dealer1.has_blackjack = False
    dealer1.is_there_a_winner = False
    #dealer1.hole_card = False
    player.hand = []
    dealer1.hand = []
    dealer1.new_hand(player, dealer1)
    dealer1.deal_cards(player, deck1)
    print("======================================================")
    player.bet = int(input("Place your bet: "))
    print("======================================================")
    #Error checking logic for betting#
    if player.bet > player.cash:
        player.bet = input("You dont have that much cash, try again: ")
    if player.bet < 0:
        player.bet = input("You cant bet anything less than 1$, try again: ")
    #Deducts bet from player bankroll
    player.cash -= player.bet
    print(f"{name}'s cards: " + str(player.hand))
    #print("Soft Hand: ", player.soft_hand)
    player.display_count()
    player.check_for_blackjack()
    #print("Count: " + str(player.display_count()) + "\n")
    print("\nThe DEALER's hand is: " + str(dealer1.hand))        
    dealer1.display_count()
    dealer1.check_for_dealer_blackjack()
    #######################################################################################
    #Here we need to only show the "top"card until it is time for the dealer to play their hand
    #if dealer1.hole_card == False:
        #print("\nThe DEALER's hand is: " + str(dealer1.hand[0]))
    #elif dealer1.hole_card == True:
        #print("\nThe DEALER's hand is: " + str(dealer1.hand))        
        #dealer1.display_count()
    #######################################################################################

    #print("Soft Hand: ", dealer1.soft_hand)
    #print("Count: " + str(dealer1.display_count()) + "\n")
    
def game_mechanics():
    #Player plays their hand first
    #Then dealer plays     
    #dealer1.hole_card == True    

    while dealer1.is_there_a_winner == False:
        if player.stay == True and dealer1.stay == True:
            dealer1.check_for_win(player, dealer1)
            dealer1.new_game()

        if player.stay == False and player.can_split == False:
            hit_stay = input("'Hit (h), Stay (s), or Double Down (d)?: ")
            if hit_stay == "s":
                player.stay = True
            elif hit_stay == "h":
                player.hit(deck1)
                dealer1.check_for_lose(dealer1, player)
                if dealer1.is_there_a_winner == True:
                    dealer1.new_game()
                else:
                    pass
            else:
                pass
        else:
            pass
        #dealer MUST hit a soft 17, so we would add this here 
        if dealer1.stay == False:
            if dealer1.card_total() <= 16:
                dealer1.hit(deck1)
                dealer1.check_for_lose(dealer1, player)
                if dealer1.is_there_a_winner == True:
                    dealer1.new_game()
            else:
                dealer1.stay = True
        else:
            pass    

begin_game()

game_mechanics()

dealer1.new_game()

#TODO
#Need to fix pop from empty list error for deck, must be reaching the end of the deck after a while and - DONE
#should call for a new deck to be created/shuffled - DONE

#Need to work on soft hand display, if hand is initially dealt with an ace, it should display 'Count x or y' ex 'Count 5 or 15'
#need to create a better method for checking for blackjack in initial hand that is dealt. a hand that adds up to 21 with more than 2 cards is not considered a 'blackjack'
#Need to start working on double down option in game
#need to start working on split hands in game
