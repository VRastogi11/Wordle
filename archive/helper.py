import random
from english_words import english_words_set

emojis = {
    'correct_place': '🟩',
    'correct_letter': '🟨',
    'incorrect': '⬜'
}

def correct_place(letter):
    return f'[black on green]{letter}[/]'

def correct_letter(letter):
    return f'[black on yellow]{letter}[/]'

def incorrect(letter):
    return f'[black on white]{letter}[/]'

def score_guess(guess, answer):
    scored = []
    emojied = []
    for i, letter in enumerate(guess):
        if answer[i] == guess[i]:
            scored += correct_place(letter)
            emojied.append(emojis['correct_place'])
        elif letter in answer:
            scored += correct_letter(letter)
            emojied.append(emojis['correct_letter'])
        else:
            scored += incorrect(letter)
            emojied.append(emojis['incorrect'])
    return ''.join(scored), ''.join(emojied)

def save_all_words():
    return list(english_words_set)

def random_word_generator():
    all_words = save_all_words()
    word = random.choice(all_words)
    while len(word) != 5:
        word = random.choice(all_words)
    return word

def process_after_guesses(used_guesses, last_guess, answer_word):
    if used_guesses == 6 and last_guess != answer_word:
        print("CORRECT WORD: ", answer_word)
        
def word_checker(word):
    all_words = save_all_words()
    if word in all_words:
        return True
    return False

def guess_validator(word):
    if word.isalpha() and word_checker(word):
        return True
    return False

