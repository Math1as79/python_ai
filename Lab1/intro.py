from colorama import init
from termcolor import cprint
import subprocess


init()

welcome = """Welcome to Game Dev Studio!
We offer the following games:
    - Hangman
    - Memory
    - Rock/Paper/Scissors
    - Black Jack

        """

cprint(welcome, "green")
play = True
while play == True:
    game = input("Choose a game(H/M/R/B): ")

    if game == "H":
        subprocess.run(["python", "hangman.py"])
    elif game == "M":
        subprocess.run(["python", "memory.py"])
    elif game == "R":
        subprocess.run(["python", "rock_paper_scissors.py"])
    elif game == "B":
        subprocess.run(["python", "blackjack.py"])

    play_again = input("Play another game? (Y/N): ")
    if play_again == "N":
        break

cprint("Thank you for playing.", "light_blue")