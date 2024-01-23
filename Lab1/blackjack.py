import random

def shuffle(deck):
    random.shuffle(deck)
    return(deck)

def deal(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card

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

player = { "sum": 0, "cards": [], "action": "hit"}
dealer = { "sum": 0, "cards": [], "action": "hit"}
deck = []
suits = ["♠", '♦', '♥', '♣']
cards = [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]

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

    while play == True:
        if player["sum"] > 21:
            play = False
            print("Game over")
        if (input(f"You have {player["sum"]}. Hit or stand (H/S)?: ")) == "H":
            player["cards"].append(deal(deck))
            player["sum"] = sum_cards(player["cards"])
        else:
            #Show dealer cards 
            if dealer["sum"] < 17:
                dealer["cards"].append(deal(deck))
                dealer["sum"] = sum_cards(dealer["cards"])
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

        
    
