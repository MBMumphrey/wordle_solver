import sys

if __name__ == "__main__":
    answers = [line.strip() for line in open(sys.argv[1])]
    guesses = [line.strip() for line in open(sys.argv[2])] + answers
    position_output = sys.argv[3]
    scores_output = sys.argv[4]

    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
               "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    positions = {x.lower():{1:0, 2:0, 3:0, 4:0, 5:0} for x in letters}

    for answer in answers:
        for i, char in enumerate(answer):
            positions[char][i + 1] += 1

    with open(position_output, 'w') as of:
        of.write(f"letter,position,count\n")
        for letter in positions.keys():
            for position in positions[letter]:
                of.write(f"{letter},{position},{positions[letter][position]}\n")

    guess_scores = {}
    for i, guess in enumerate(guesses):
        if i % 100 == 0:
            print(i)
        scores = []
        for answer in answers:
            score = 0
            for j, g in enumerate(guess):
                if g == answer[j]:
                    score += 3
                elif answer.find(g) != -1:
                    score += 1
                else:
                    score += 0
            scores.append(score)
        guess_scores[guess] = sum(scores)/len(scores)

    with open(scores_output, 'w') as of:
        of.write(f"guess,av_score\n")
        for guess in guess_scores.keys():
            of.write(f"{guess},{guess_scores[guess]}\n")