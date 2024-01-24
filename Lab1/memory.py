import random
import string
import sys, time 

print("Let's play memory")
level = input("Choose your level of memory (Easy/Medium/Hard/Impossible)")

if level == "Easy":
    guesses_and_time = 3
    memory_string = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
elif level == "Medium":
    guesses_and_time = 5
    memory_string = ''.join(random.sample(string.ascii_letters, k=10))
elif level == "Hard":
    guesses_and_time = 7
    memory_string = ''.join(random.choices(string.ascii_letters + string.digits, k=20)) 
elif level == "Impossible":
    guesses_and_time = 10
    memory_string = ''.join(random.choices(string.ascii_letters + string.digits, k=50)) 


print(f"Remember: {memory_string}, you have {guesses_and_time} seconds..", end="")
print("\r", end="")
time.sleep(guesses_and_time)

print(f"The rearranged string: {''.join(random.sample(memory_string,len(memory_string)))}, you have {guesses_and_time} guesses..")

while guesses_and_time > 0:
    guess = input("Can you remember the correct order?: ")
    if guess == memory_string:
        print("Correct")
        break
    else:
        guesses_and_time -= 1
        print("Wrong")

print("Game finished")