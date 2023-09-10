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
    
    def shufffle_deck(self):
        random.shuffle(self.cards) 

#Next, is the player class
#Players have a name, an amount of cash, and they will have a hand of cards dealt to them 
#Players can choose how much they bet, if they want to make side bets, hit, stay, split cards, or double down. 
class Player:
    def __init__(self, name, cash = 0):
        self.cards = []
        self.cash = cash
        self.name = name 
        self.stay = False
        self.double_down = False
        #we have to remember that you typically cannot double down on a split
        self.split_cards = False
        
    def hit(self, deck):
        self.cards.append(deck.deal_card())
        print(f"{self.name}'s cards: " + str(self.cards))
        print("Count: " + str(self.calculate_hand()) + "\n")
        
    def card_total(self):
        total = 0
        for card in self.cards:
            if card[0] == 'J':
                total += 10
            elif card[0] == 'Q':
                total += 10
            elif card[0] == 'K':
                total += 10
            elif card[0] == 'A':
                total += 11
            else:
                total += card[0]

        return total
    
    def show_cards(self):
        for card in self.cards:
            return str(card[0]) + " of " + str(card[1]) 
        
    