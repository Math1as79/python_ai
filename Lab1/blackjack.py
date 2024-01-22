import random

def deal(deck):
    type = random.choice(list(deck.keys()))
    card = random.choice(list(deck.values()))
    print(type, card)

cards = [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]
deck = {"hearts": cards, "spades": cards, "clubs": cards, "diamonds": cards} 

deal(deck)


