from random import randint

handsigns = ["rock","paper","scissors"]

print(f"Lets play {handsigns[0]}/{handsigns[1]}/{handsigns[2]}")

human_handsign = input("Choose a handsign:")

computer_handsign = handsigns[randint(0,len(handsigns)-1)]

print(f"Your handsign is {human_handsign}, computer handsign is {computer_handsign}")

if human_handsign == computer_handsign:
    print("It's a tie.")
elif human_handsign == "rock" and computer_handsign == "scissors":
    print ("You win.")
elif human_handsign == "scissors" and computer_handsign == "paper":
    print ("You win.")
elif human_handsign == "paper" and computer_handsign == "rock":
    print ("You win.")
else:
    print("Computer win.")