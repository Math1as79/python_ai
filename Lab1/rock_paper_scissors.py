from random import randint

handsigns = ["rock","paper","scissors"]

print(f"Lets play {handsigns[0]}/{handsigns[1]}/{handsigns[2]}")

play = True 
while play == True :
    human_handsign = input("Choose a handsign:")
    computer_handsign = handsigns[randint(0,len(handsigns)-1)]

    print(f"Your handsign is {human_handsign}, computer handsign is {computer_handsign}")

    if human_handsign == computer_handsign:
        print("It's a tie.")
    elif human_handsign == "rock" and computer_handsign == "scissors":
        play = False
        print ("You win.")
    elif human_handsign == "scissors" and computer_handsign == "paper":
        play = False
        print ("You win.")
    elif human_handsign == "paper" and computer_handsign == "rock":
        play = False
        print ("You win.")
    else:
        play = False
        print("Computer win.")

print("Game finished")