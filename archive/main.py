from rich.prompt import Prompt
from rich.console import Console
from helper import (
    correct_place,
    guess_validator, 
    incorrect, 
    score_guess, 
    correct_letter, 
    random_word_generator, 
    word_checker
    )

WELCOME_MESSAGE = correct_place("WELCOME") + " " + incorrect("TO") + " " + correct_letter("TWORDLE") + "\n"
P_INSTRUCTIONS = "Player: You may start guessing\n"

def main():
    allowed_guesses = 6
    used_guesses = 0

    console = Console()
    console.print(WELCOME_MESSAGE)

    answer_word = random_word_generator()
    console.clear()
    console.print(WELCOME_MESSAGE)
    console.print(P_INSTRUCTIONS)

    all_emojied = []
    all_scored = []
    last_guess = ''
    while used_guesses < allowed_guesses:
        used_guesses += 1
        guess = Prompt.ask("Enter your guess")
        while True:
            if len(guess) == 5 and guess_validator(guess):
                break
            elif len(guess) != 5:
                console.clear()
                console.print(WELCOME_MESSAGE)
                print("Word length should be 5")
            else:
                console.clear()
                console.print(WELCOME_MESSAGE)
                print("Your guess is invalid")
                print()
            guess = Prompt.ask("Enter your guess again")

        scored, emojied = score_guess(guess, answer_word)
        all_scored.append(scored)
        all_emojied.append(emojied)
        console.clear()
        console.print(WELCOME_MESSAGE)
        for scored in all_scored:
            console.print(scored)

        print("Remaining guesses: ", allowed_guesses - used_guesses)
        if guess == answer_word:
            print("Guess Word is a Correct Word")
            break
        else:
            if used_guesses == 6:
                print("CORRECT WORD: ", answer_word)
            if word_checker(guess):
                print("Guess Word is a Valid Word but incorrect")
        last_guess = guess
    print(f"\n\nTWORDLE {used_guesses}/{allowed_guesses}\n")

    for em in all_emojied:
        console.print(em)
    

if __name__ == '__main__':
    main()