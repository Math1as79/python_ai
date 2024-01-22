from random import randint

max_guesses = 0
guessed_word = []

# function to validate the input, using lower because in is case sensitive 
def __validate_char(char):
    if char.lower() in word:
       return True
    else: 
        return False
    

words = ["apple", "orange", "car", "airplane", "boat"]

#take a random word in the list 
word = (words[randint(0,len(words)-1)])

#create a list of x to be able to replace values in list with correct characters
for w in word:
    guessed_word.append("x")

#setting the max guesses to choosen word multiplied by two
max_guesses = len(words) * 2

print ("Let's play hangman.")

print(f"Word contains {str(len(word))} characters. You have {max_guesses} before you lose. ")

#looping guesses and deduct one on every wrong guess
while max_guesses >= 0:
    char = input("Guess a character:")
    if len(char) != 1:
        print("You can only type one character at the time. Try again.")
    else:
        validation = __validate_char(char)
        if validation == True:
            for i in range(len(word)):
                if char == word[i]:
                    guessed_word[i] = char
            print("You found one or more characters in the word: " + ''.join(guessed_word))
        else: 
            max_guesses -= 1
            print(f"You have {max_guesses} guesses left. Try again.")
        
        if ''.join(guessed_word) == word:
            print(f"You have won. Correct word {word}")
            break 
        

