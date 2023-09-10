import random

#Here is where I create a deck of cards using 3 lists
number = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A", "J", "Q", "K"]
suits = [u"\u2663", u"\u2660", u"\u2666", u"\u2665"]
#using list comprehension to create the 52 playable cards
deck = [[x, y] for x in number for y in suits]

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
    
    #This method is helpful for splits
    def add_card(self, cards):
        self.cards.append(cards)
        return self.cards
    
    def shufffle_deck(self):
        random.shuffle(self.cards) 

#Next, is the player class
#Players have a name, an amount of cash, and they will have a hand of cards dealt to them 
#Players can choose how much they bet, if they want to make side bets, hit, stay, split cards, or double down. 
class Player:
    def __init__(self, name, cash = 0, bet = 0):
        self.cards = []
        self.split = []
        self.cash = cash
        self.name = name 
        self.bet = bet
        self.num_aces = 0
        self.stay = False
        #players can double their original bet, and a hit must be made
        self.double_down = False
        self.can_double = True
        #we have to remember that you typically cannot double down on a split
        self.split_cards = False
        self.can_split = False
        #Any hand with an Ace is considered a 'soft' hand
        self.soft_hand = False
            
    def hit(self, deck):
        self.cards.append(deck.deal_card())
        print(f"{self.name}'s cards: " + str(self.cards))
        total = self.card_total()
        if self.soft_hand == False:
            print("Count: " + str(total + "\n"))
        elif self.num_aces == 1:
            print("Count: " + str(total) + " or " + str(total - 10)+ "\n")
        elif self.num_aces == 2: 
            print("Count: " + str(total - 10) + " or " + str(total - 20)+ "\n")
        
    def card_total(self):
        total = 0
        for card in self.cards:
            if card[0] == 'J':
                total += 10
            elif card[0] == 'Q':
                total += 10
            elif card[0] == 'K':
                total += 10
            #Aces are 1 or 11, any hand with an Ace is considered a 'soft' hand
            elif card[0] == 'A':
                total += 11
                self.soft_hand = True
                self.num_aces += 1
            else:
                total += card[0]

        return total
    
    def split_cards(self, deck):
        self.split_cards = True
        self.can_double = False
        self.cash -= self.bet
        self.split.append(self.cards.pop())
        self.cards.append(deck.deal_card())
        self.split.append(deck.deal_card())
        
        #self.split.append(self("Split 1: ", deck, self.bet))
        #self.split.append(self("Split 2: ", deck, self.bet))
        #for i in self.split:
            #i.add_card(self.cards.pop(0))
            #i.add_card(deck.deal_card())
            
    
    def show_cards(self):
        for card in self.cards:
          return str(card[0]) + " of " + str(card[1]) 
        
#The Dealer is technically a player in the game. So the Dealer class is a subclass of Player
#A dealer can: Deal cards, Check for win/losses
#The dealer must hit a soft 17
class Dealer(Player):
    def __init__(self, name, cash=0):
        super().__init__(name)
        self.cards = []
        self.is_winner = False

    def deal_cards(self, player, deck):
        player.cards.append(deck.deal_card())
        player.cards.append(deck.deal_card())
        self.hand.append(deck.deal_card())
        self.hand.append(deck.deal_card())

#Check for winner
    def check_for_win(self, player, dealer):
        if int(player.card_total()) > 21 or int(
                dealer.card_total()) == 21 or int(
                dealer.card_total()) > int(player.card_total()):
            print(f"{player.name} Loses")
            self.is_there_a_winner = True

        elif int(dealer.card_total()) > 21 or int(
                player.card_total()) == 21 or int(
                player.card_total()) > int(dealer.card_total()):
            print(f"{player.name} wins")
            self.is_there_a_winner = True
        else:
            print("Push")
            self.is_there_a_winner = True

#Check for bust
    def check_for_lose(self, player):
        if int(player.card_total()) > 21:
            print(f"{player.name} Loses")
            self.is_there_a_winner = True

        else:
            pass

    def new_hand(self, player, dealer):
        player.hand = []
        dealer.hand = []

    def new_game(self):
        another_game = input("Play another round?  y/n:  ")
        if another_game == "y":
            begin_game()
        else:
            pass
   
        
dealer1 = Dealer("Dealer")
deck1 = Deck(deck)
deck1.shuffle_deck()
name = input("Please input your name: ")
player = Player(name, 200)
print("`~*- BLACKJACK -*~`\n")
print(f"\n Welcome {name}!\n")

def begin_game():
    player.stay = False
    dealer1.stay = False
    dealer1.is_there_a_winner = False
    player.hand = []
    dealer1.hand = []
    dealer1.new_hand(player, dealer1)
    dealer1.deal_cards(player, deck1)
    print(f"{name}'s hand is: " + str(player.hand))
    print("Count: " + str(player.calculate_hand()) + "\n")
    print("\nThe DEALER's hand is: " + str(dealer1.hand))
    print("Count: " + str(dealer1.calculate_hand()) + "\n")
    
def game_mechanics():
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
                dealer1.check_for_lose(player)
                if dealer1.is_there_a_winner == True:
                    dealer1.new_game()
                else:
                    pass
            else:
                pass
        else:
            pass
        
        if dealer1.stay == False:
            if dealer1.calculate_hand() <= 16:
                dealer1.hit(deck1)
                dealer1.check_for_lose(dealer1)
                if dealer1.is_there_a_winner == True:
                    dealer1.new_game()
            else:
                dealer1.stay = True
        else:
            pass    