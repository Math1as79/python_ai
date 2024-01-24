import random

#Shuffle the deck with imported function random
def shuffle(deck):
    random.shuffle(deck)
    return(deck)

#Take random card from the deck and remove it from the deck as well
def deal(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card

#Summarize the sum of the hand of the individual player
def sum_cards(cards):
    card_sum = 0
    for card in cards:
        if card[1].isnumeric() == True:
            card_sum = card_sum + int(card[1:])
        elif card[1] == "A":
            card_sum = card_sum + 11
        else:
            card_sum = card_sum + 10
    
    return card_sum

player = { "sum": 0, "cards": []}
dealer = { "sum": 0, "cards": []}
deck = []
suits = ["♠", '♦', '♥', '♣']
cards = [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]
action = "H"

#Creating the deck 
for suit in suits:
    for card in cards:
        deck.append(suit + str(card))

if (input("Would you like to play black jack (Y/N)?: ")) == "Y":
    play = True
    shuffle(deck)
    for i in range(2):
        player["cards"].append(deal(deck))
        player["sum"] = sum_cards(player["cards"])
        dealer["cards"].append(deal(deck))
        dealer["sum"] = sum_cards(dealer["cards"])
        i += 1
    
    #Important when we call sum_cards that we send in a list
    print(f"You have {' '.join(player["cards"])} Sum: {player["sum"]}  | ", f"Dealer has {dealer["cards"][0]} Sum: {sum_cards([dealer["cards"][0]])}")
    
    while play == True:
        if player["sum"] > 21:
            play = False
            print(f"Game over: You have more than 21 => {player["sum"]}")
            break
        if action == "H":
            if (input(f"Hit or stand (H/S)?: ")) == "H":
                player["cards"].append(deal(deck))
                player["sum"] = sum_cards(player["cards"])
                print(f"You have {' '.join(player["cards"])} Sum: {player["sum"]}.")
            else:
                action = "S"
                print(f"Dealer has {' '.join(dealer["cards"])} Sum: {dealer["sum"]}.")
        else:
            if dealer["sum"] < 17:
                dealer["cards"].append(deal(deck))
                dealer["sum"] = sum_cards(dealer["cards"])
                print(f"Dealer has {' '.join(dealer["cards"])} Sum: {dealer["sum"]}.")
            else: 
                play = False
                if dealer["sum"] > 21:
                    print(f"You win {player["sum"]} against dealer {dealer["sum"]}")
                elif player["sum"] > dealer["sum"]:
                    print(f"You win {player["sum"]} against dealer {dealer["sum"]}")
                elif player["sum"] < dealer["sum"]:
                    print(f"You lose {player["sum"]} against dealer {dealer["sum"]}")
                else:
                    print("Tie")
        
    print("Game finished")

        
    
