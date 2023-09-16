import random

#DECK OF CARDS ARE ALWAYS GOING TO HAVE THESE VALUES, 52 CARDS, 4 SUITS ETC
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
        return pick
    
    def shuffle_deck(self):
        random.shuffle(self.cards) 
    
    def new_deck(self):
        self.cards = self.create_deck()    
        
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
        
        print("Count: " + str(self.card_total()) + "\n")
        
    #If any player's hand contains an Ace, it is considered a "soft" hand
    #We can check for that with this method
    def check_for_soft_hand(self):
        for card in self.hand:
            if card[0] == 'A':
                self.soft_hand = True
                

    #A player must be able to calculate the card total in their hand
    def card_total(self):
        total = 0
        for card in self.hand:
            if card[0] == 'A':
                total += 11
            elif card[0] == 'K':
                total += 10
            elif card[0] == 'Q':
                total += 10    
            elif card[0] == 'J':
                total += 10                
            else:
                total += card[0]
        #Here we call our method for checking for a soft hand, 
        #so if there isnt a blackjack, it is considered a soft hand
        self.check_for_soft_hand()        
        #if the hand is a soft hand, we deduct 10 from the card total if
        #the hand is totaled over 21, known as a "free hit" in real life Blackjack
        if total > 21:
            if self.soft_hand == True:
                return total - 10
            else:
                return total

        return total
    
    #A player must check to see if they have blackjack
    #TODO: would love to add a feature to "take even money" 
    #when player has blackjack and suspects dealer to have blackjack before revealing "hole card"
    def check_for_blackjack(self):
        if self.card_total() == 21:
            self.has_blackjack = True
            
    #Display format for count, useful for soft hands too. 
    def display_count(self):
        total = self.card_total()
        print("Soft Hand: ", self.soft_hand)
        if self.soft_hand == True:
            if total < 21:
                print("Count: " + str(total) + " or " + str(total - 10)+ "\n")                
            elif total > 21:
                print("Count: " + str(total - 10) + "\n")
        else:
            print("Count: " + str(total) + "\n")  
    
#Next is the Dealer class. A dealer in blackjack is considered a Player of the game, 
#so it will "inherit" any attributes of a player           
class Dealer(Player):
    
    #The "hole card" is the card that stays face down before the dealer plays their hand, 
    #once it is time for the dealer to play their hand, they reveal their second card

    #TODO: Add feature for hole card, which is the face down card in real life blackjack,
    #being revealed after the player decides how to play
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
        
    #Here we need to check for dealer blackjack
    #When hole card is enabled, the dealer checks for blackjack
    #after the player makes their first decision/play.
    #This will play a part in revealing the hole card
    def check_for_dealer_blackjack(self, player):
        if player.has_blackjack == True and self.has_blackjack == False:
            print("BLACKJACK!")
            print(f"{player.name} wins {player.bet * 1.5}$!")
            player.cash += (player.bet * 2.5)
            print(f"Cash {player.cash}$")
            self.is_there_a_winner = True            
            self.new_game()               
        elif self.has_blackjack == True:
            if player.has_blackjack == False:
                print("Dealer has Blackjack!")
                print(f"{player.name} Loses \nCash: {player.cash}")
                self.is_there_a_winner = True                
                self.new_game()
            elif player.has_blackjack == True:
                player.cash += player.bet
                print("Push \nCash: " + str(player.cash))
                self.is_there_a_winner = True
                self.new_game()
            
    #CHECK FOR BUST#######################################    
    def check_for_bust(self, dealer, player):
        #If player busts, player Loses
        if int(player.card_total()) > 21:
            print(f"{player.name} Loses \nCash: {player.cash}")
            self.is_there_a_winner = True
        #If dealer busts, Player Wins   
        elif int(dealer.card_total()) > 21:
            print(f"{player.name} wins {player.bet}$!")
            player.cash += (player.bet * 2)
            print(f"Cash {player.cash}$")
            self.is_there_a_winner = True
        else:
            pass
        
   #Dealer must be able to check for any wins/losses 
    def check_for_win(self, player, dealer):
        #21 PUSH##############################################
        #if both the dealer and player have 21, it is a PUSH
        if int(dealer.card_total()) == 21 and int(player.card_total()) == 21:
            player.cash += player.bet
            print("Push \nCash: " + str(player.cash))
            self.is_there_a_winner = True
            
        #21 CHECKING##########################################   
        #If player has 21, and dealer does not, then player WINS - DONE
        elif int(player.card_total()) == 21 and not int(dealer.card_total()) == 21:
            print(f"{player.name} wins {player.bet}$!")
            player.cash += (player.bet * 2)
            print(f"Cash {player.cash}$")
            self.is_there_a_winner = True 
            
        #If dealer has 21, and player does not,then player LOSES - DONE
        elif int(dealer.card_total()) == 21 and not int(player.card_total()) == 21:
            print(f"{player.name} Loses \nCash: {player.cash}")
            self.is_there_a_winner = True  
            



        
        #IF NO BUST, CHECK WHOS TOTAL IS HIGHER################
        #If both player and dealer card totals are under 21
        elif int(player.card_total()) < 21 and int(dealer.card_total()) < 21:
            #Check to see if dealer has higher total, Player Lose
            if int(dealer.card_total()) > int(player.card_total()):
                print(f"{player.name} Loses \nCash: {player.cash}")
                self.is_there_a_winner = True
            #Check to see if player has higher total, Player Win
            elif int(player.card_total()) > int(dealer.card_total()):
                print(f"{player.name} wins {player.bet}$!")
                player.cash += (player.bet * 2)
                print(f"Cash {player.cash}$")
                self.is_there_a_winner = True
            #CHECK FOR PUSH########################################
            #If the player and dealer card totals are the same, then it is a PUSH
            elif int(player.card_total()) == int(dealer.card_total()):
                player.cash += player.bet
                print("Push! \nCash: " + str(player.cash))
                self.is_there_a_winner = True
            
    def new_game(self):
        print("======================================================")
        another_game = input("Play another round?  y/n:  ")
        if another_game == "y":
            play_game()
        else:
            pass     

print("`~*- BLACKJACK -*~`\n")
name = input("Please input your name: ")
print(f"\nWelcome {name}!\n")
player = Player(name, 200)

def play_game():
    dealer = Dealer("Dealer")
    deck = Deck(create_deck())
    deck.shuffle_deck()    
    player.bet = 0
    player.stay = False
    dealer.stay = False
    player.soft_hand = False
    dealer.soft_hand = False
    player.has_blackjack = False
    dealer.has_blackjack = False
    dealer.is_there_a_winner = False
    dealer.hole_card = False
    player.hand = []
    dealer.hand = []
    dealer.deal_cards(player, deck)
    print("======================================================")
    player.bet = int(input("Place your bet: "))
    print("======================================================")
    #Error checking logic for betting#
    if player.bet > player.cash:
        player.bet = input("You dont have that much cash, try again: ")
    if player.bet < 0:
        player.bet = input("You cant bet anything less than 1$, try again: ")
    #Deducts bet from player bankroll#
    player.cash -= player.bet 
    print(f"{name}'s hand: " + str(player.hand))
    #print("Soft Hand: ", player.soft_hand)
    player.display_count()
    #print("Count: " + str(player.display_count()) + "\n")
    print("\nThe DEALER's hand is: " + str(dealer.hand[0]))        
    dealer.display_count()
    
    player.check_for_blackjack()
    dealer.check_for_blackjack()
    dealer.check_for_dealer_blackjack(player) 
    dealer.hole_card = True

    while dealer.is_there_a_winner == False:
          
        if player.stay == True and dealer.stay == True:
            dealer.check_for_win(player, dealer)
            dealer.new_game()

        if player.stay == False and player.can_split == False:
            hit_stay = input("'Hit (h), Stay (s), or Double Down (d)?: ")
            if hit_stay == "s":
                player.stay = True
            elif hit_stay == "h":
                player.hit(deck)
                dealer.check_for_bust(dealer, player)
                if dealer.is_there_a_winner == True:
                    dealer.new_game()
                else:
                    pass
            else:
                pass
        else:
            pass

        if dealer.stay == False:
            #DEALER MUST HIT SOFT 17, just like in real life
            if dealer.soft_hand == True and dealer.card_total == 17:
                dealer.hit(deck)
                dealer.check_for_win(player, dealer)
                if dealer.is_there_a_winner == True:
                    dealer.new_game()
            #while dealer.card_total() < 17:
                #dealer.hit(deck)                
            if dealer.card_total() <= 16:
                dealer.hit(deck)
                dealer.check_for_bust(dealer, player)
                if dealer.is_there_a_winner == True:
                    dealer.new_game()
            else:
                dealer.stay = True
        else:
            pass

play_game()