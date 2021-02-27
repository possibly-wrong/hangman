from collections import defaultdict, Counter
import random

max_misses = 10
words = []
with open('words.txt') as f:
    for line in f:
        word = line.strip()
        patterns = defaultdict(tuple)
        for i, letter in enumerate(word):
            patterns[letter] += (i,)
        words.append((word, patterns))
n = random.choice([len(word) for word, patterns in words])
possible = [(word, patterns) for word, patterns in words if len(word) == n]
word = ['-'] * n
misses = []
while len(misses) < max_misses and '-' in word:
    prompt = '{} (missed [{}]), enter guess: '.format(''.join(word).upper(),
                                                      ''.join(misses))
    guess = input(prompt).lower()
    pattern = Counter(patterns[guess]
                      for word, patterns in possible).most_common(1)[0][0]
    possible = [(word, patterns)
                for word, patterns in possible if patterns[guess] == pattern]
    for i in pattern:
        word[i] = guess
    if not pattern:
        misses.append(guess)
        print('  No {}, {} misses remaining.'.format(guess.upper(),
                                                     max_misses - len(misses)))
print('The word was', possible[0][0].upper())
