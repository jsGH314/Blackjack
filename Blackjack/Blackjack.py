import random

#Here is where I create a deck of cards using 3 lists
number = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A", "J", "Q", "K"]
suits = [u"\u2663", u"\u2660", u"\u2666", u"\u2665"]
#using list comprehension to create the 52 playable cards
deck = [[x, y] for x in number for y in suits]

#The Deck class will feature actions that a deck of cards is capable of via a "Dealer" class
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
