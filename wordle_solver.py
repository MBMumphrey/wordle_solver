import sys
import re
import random
from collections import Counter

class Wordle:
    def __init__(self, answer):
        self.pattern = "?????"
        self.present = []
        self.absent = []
        self.regex = ".*"
        self.answer = answer
        self.guesses = []

    def make_regex(self):
        absent_string = "".join(set(self.absent))
        lookahead_string = "".join([f"(?=.*{c})" for c in set(self.present)])
        self.regex = lookahead_string + self.pattern.replace("?", f"[^Z{absent_string}]")

    def check_guess(self, guess):
        self.guesses.append(guess)
        for j, g in enumerate(guess):
            if g == self.answer[j]:
                self.pattern = self.pattern[:j] + g + self.pattern[j+1:]
                self.present.append(g)
            elif self.answer.find(g) != -1:
                self.present.append(g)
            else:
                self.absent.append(g)

def find_guess(current_answers):
    #Give wrong letters a slightly positive score based on how many words they remove
    #from the pool when found to be wrong.
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
               "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    letter_scores = {c:len([x for x in current_answers if x.find(c) != -1])/len(current_answers) for c in letters}
    best_score = 0
    best_word = ""
    for i, word_1 in enumerate(current_answers):
        scores = []
        for word_2 in current_answers:
            score = 0
            for j, g in enumerate(word_1):
                if g == word_2[j]:
                    score += 4
                elif word_2.find(g) != -1:
                    score += 1
                else:
                    score += letter_scores[g]
            scores.append(score)
        av_score = sum(scores)/len(scores)
        if av_score > best_score:
            best_word = word_1
            best_score = av_score
    return best_word

if __name__ == "__main__":
    possible_answers = [line.strip() for line in open(sys.argv[1])]
    guess_counts = Counter()

    for i, answer in enumerate(possible_answers):
        if i % 100 == 0:
            print(i)
        current_answers = possible_answers
        run = Wordle(answer)
        #first guess based on previous analysis of which words give the best starting information
        best_guess = "saree"
        j = 1
        while(len(current_answers) > 1):
            run.check_guess(best_guess)
            run.make_regex()
            #print(f"\t{j} - {best_guess} - {run.pattern}")
            current_answers = [x for x in list(filter(re.compile(run.regex).match, current_answers)) if not x in run.guesses]
            if (len(current_answers) > 1):
                best_guess = find_guess(current_answers)
            else:
                guess_counts.update([j])
                break
            j += 1

    print(sorted(guess_counts.items()))
        
