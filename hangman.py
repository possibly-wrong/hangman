from collections import defaultdict, Counter
from itertools import groupby
import random

def load_dictionary(filename):
    with open(filename) as f:
        for line in f:
            word = line.strip()
            pattern = defaultdict(tuple)
            for i, letter in enumerate(word):
                pattern[letter] += (i,)
            yield (word, pattern)

def human_guess(prompt, guessed, missed, possible, show):
    return input(prompt).lower()

def best_guess(prompt, guessed, missed, possible, show):
    used = set(guessed) | set(missed)
    guess = Counter(letter for word, pattern in possible for letter in pattern
                    if pattern[letter] and
                    letter not in used).most_common(1)[0][0]
    if show:
        print('{}{}'.format(prompt, guess))
    return guess

def play(guesser, max_misses, words, secret, show=True):
    n = len(secret)
    guessed = ['-'] * n
    missed = []
    possible = [(word, pattern) for word, pattern in words if len(word) == n]
    while len(missed) < max_misses and '-' in guessed:
        prompt = '{} (missed [{}]), guess: '.format(''.join(guessed).upper(),
                                                    ''.join(missed))
        guess = guesser(prompt, guessed, missed, possible, show)

        # Maximize number of remaining possible words.
        scores = Counter(pattern[guess] for word, pattern in possible
                         if '-' in secret or word == secret).most_common()

        # Break ties with fewest new letters (miss if possible).
        score = min(next(groupby(scores, key=lambda c: c[1]))[1])[0]
        possible = [(word, pattern) for word, pattern in possible
                    if pattern[guess] == score]
        for i in score:
            guessed[i] = guess
        if not score:
            missed.append(guess)
            if show:
                print('    No {}, {} misses remaining.'.format(
                    guess.upper(), max_misses - len(missed)))
    secret = possible[0][0] if '-' in secret else secret
    if show:
        print('The word was', secret.upper())
    return guessed, missed, secret

if __name__ == '__main__':
    words = list(load_dictionary('words.txt'))
    while True:
        play(human_guess, 10, words, '-' * len(random.choice(words)[0]))
