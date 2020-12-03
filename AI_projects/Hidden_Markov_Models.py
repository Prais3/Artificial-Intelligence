############################################################
# CMPSC 442: Homework_6
############################################################

# student_name = "Varun Jani"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from collections import defaultdict

############################################################
# Section 1: Hidden Markov Models
############################################################

tags = ('NOUN', 'VERB', 'ADJ', 'ADV', 'PRON', 'DET', 'ADP', 'NUM', 'CONJ',
        'PRT', '.', 'X')


# This function loads the corpus to the given path and returns the list of POS-tagged sentences
def load_corpus(path):
    with open(path, 'r+') as f:
        return [[tuple(token.split('=')) for token in line.split()] for line in f]


class Tagger(object):

    # This one initializes for a, b and pi, the probabilities and takes the list of sentences from load_corpus function
    def __init__(self, sentences):
        self.pi_dict = {}
        self.a_dict = {}
        self.b_dict = {}
        count = 0.0

        for t in tags:
            self.pi_dict[t] = 0
            self.a_dict[t] = {}

            for t2 in tags:
                self.a_dict[t][t2] = 0
            self.b_dict[t] = defaultdict(float)

        for words in sentences:
            (x, tag) = words[0]
            self.pi_dict[tag] += 1

            for i in range(len(words)):
                (x, tag) = words[i]
                (x, last_tag) = words[i - 1]
                self.a_dict[last_tag][tag] += 1

            for (token, tag) in words:
                self.b_dict[tag][token] += 1

        # For loop based on Laplace smoothing
        for t in tags:
            # This is for the initial tag probability pi where pi smoothness is 1e-10
            count += self.pi_dict[t] + 1e-10
            self.pi_dict[t] = float(self.pi_dict[t] + 1e-10) / count

            # This is for the transition probability a where a smoothness is 1e-10
            for t2 in tags:
                count += self.a_dict[t][t2] + 1e-10
                self.a_dict[t][t2] = float(self.a_dict[t][t2] + 1e-10) / count

            # This is for the emission probability b where b smoothness is 1e-10 again
            count = 1e-10
            for token in self.b_dict[t]:
                count += self.b_dict[t][token]
                self.b_dict[t][token] = float(self.b_dict[t][token] + 1e-10) / count
            self.b_dict[t]["<UNK>"] = float(1e-10 / count)

    # This function based on the tokens sent in, returns a list of the most probable tags
    def most_probable_tags(self, tokens):
        most_prob_list = []
        if tokens:
            for t in tokens:
                state = ""
                prob = -1
                for x in tags:
                    if t not in self.b_dict[x]:
                        val = self.b_dict[x]["<UNK>"]
                    else:
                        val = self.b_dict[x][t]
                    if prob < val:
                        prob = val
                        state = x
                most_prob_list.append(state)
            return most_prob_list
        else:
            return []

    # This function uses the Viterbi coding to find the most probable tag sequence
    def viterbi_tags(self, tokens):
        gamma = [[0.0 for _ in tags] for _ in tokens]
        alpha = [[0 for _ in tags] for _ in tokens]

        # Simply checking like the most probable function is tokens are there or not
        if tokens:
            tags_range = range(len(tags))
            for i in tags_range:
                # Checking the initial tag probabilities
                if tokens[0] in self.b_dict[tags[i]]:
                    b = self.b_dict[tags[i]][tokens[0]]
                else:
                    b = self.b_dict[tags[i]]["<UNK>"]

                gamma[0][i] = self.pi_dict[tags[i]] * b

            # Looking for the most probable tag sequence, there are two parts to this though
            for t in range(1, len(tokens)):
                for j in tags_range:
                    state = 0
                    prob = -1
                    for i in range(len(tags)):
                        val = gamma[t - 1][i] * self.a_dict[tags[i]][tags[j]]

                        if prob < val:
                            prob = val
                            state = i

                    alpha[t][j] = state

                    if tokens[t] in self.b_dict[tags[j]]:
                        b = self.b_dict[tags[j]][tokens[t]]
                    else:
                        b = self.b_dict[tags[j]]["<UNK>"]

                    gamma[t][j] = prob * b

            # This part will allow me to to achieve the probability from end to beginning by tracing backpointers
            state = 0
            prob = -1
            path = []
            for i in tags_range:
                if gamma[-1][i] > prob:
                    prob = gamma[-1][i]
                    state = i

            path.append(tags[state])
            for t in range(len(tokens) - 2, -1, -1):
                state = alpha[t + 1][state]
                path.append(tags[state])

            final = list(reversed(path))
            return final
        else:
            return []


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Around 6-7 hours to complete the assignment
"""

feedback_question_2 = """
I think the most challenging part was the init function. Once that was done, it wasn't as bad after.
And no there weren't any significant stumbling blocks.
"""

feedback_question_3 = """
This assignment was alright. I don't think I would have changed anything as much.
"""
