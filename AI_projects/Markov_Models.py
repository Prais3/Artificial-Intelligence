############################################################
# CMPSC 442: Homework 5
############################################################

# student_name = "Varun Jani"


############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from random import random
from math import exp, log
from string import punctuation


############################################################
# Section 1: Markov Models
############################################################

# Function tokenize where we input a string of text and return the tokens derived from the list
def tokenize(text):
    updated_text = text.strip().split()
    tokens_list = []

    for char in updated_text:
        for c in char:
            if c in punctuation:
                tokens_list.append(" {} ".format(c))
            else:
                tokens_list.append(c)
        tokens_list += [" "]

    res = "".join(tokens_list).split()
    return res


# Function ngrams which produces a list of all the n-grams from input token list of specified size
def ngrams(n, tokens):
    first, last = 0, n - 1
    tokens += ["<END>"]
    initial = tuple(["<START>"] * (n - 1) + tokens)
    ng_list = []

    # For loop to iterate through the tokens and append to the list
    for x in tokens:
        ng_list.append((initial[first:last], x))
        first += 1
        last += 1
    return ng_list


# The NgramModel class
class NgramModel(object):

    # Simple initialization
    def __init__(self, n):
        self.n = n
        self.ng_total = {}
        self.val = False
        self.gram = set()
        self.x = tuple(["<START>"] * (self.n - 1))

    # This function computes the n-grams and updates based on the internal counts
    def update(self, sentence):
        # Checking for case when n is equal to 1
        if self.n == 1:
            self.val = True

        for c, t in ngrams(self.n, tokenize(sentence)):
            # To keep count and insert the relevant data
            if c in self.ng_total:
                if t in self.ng_total[c]:
                    self.ng_total[c][t] += 1
                else:
                    self.ng_total[c][t] = 1
            else:
                self.ng_total[c] = {t: 1}

    # This function returns the probability of that token occuring when given a tuple with context and token
    def prob(self, context, token):

        # Simply check if the token is there or not before checking for context
        if token not in self.ng_total[context]:
            return 0.0

        # Check for both and do the appropriate calculations
        if context in self.ng_total:
            if token in self.ng_total[context]:
                final = sum(self.ng_total[context].values())
                return float(1.0 * (self.ng_total[context][token]) / final)
        else:
            return 0.0

    # This function simply returns a random token using random function
    def random_token(self, context):
        rand = random()
        sum_p = 0

        # To check based on the given context
        if context in self.ng_total:
            if self.n == 1 and self.val:
                self.gram = sorted(set(self.ng_total[context].keys()))
                count_tok = self.gram
                self.val = False
            elif self.n != 1 and self.val:
                count_tok = sorted(set(self.ng_total[context].keys()))
                self.val = False
            elif self.n == 1:
                count_tok = self.gram
            else:
                count_tok = sorted(set(self.ng_total[context].keys()))
        else:
            return None

        for t in count_tok:
            p = self.prob(context, t)
            total = p + sum_p

            # Return the number of tokens
            if sum_p < rand < total:
                return t
            sum_p += p

    # This function returns a string of space-separated tokens which are again chosen at random from the
    # previous function which already uses random function
    def random_text(self, token_count):
        list_tokens = []

        for i in range(token_count):
            token_rand = self.random_token(self.x)
            list_tokens += [token_rand]

            if token_rand == "<END>":
                self.x = tuple(["<START>"] * (self.n - 1))
            elif self.n != 1:
                self.x = self.x[1:] + (token_rand,)

        final = " ".join(list_tokens)
        return final

    # This function computes the n-gram for the input sentence and returns their perplexity based on the current model
    def perplexity(self, sentence):
        ng = ngrams(self.n, tokenize(sentence))
        result = float(exp(-sum(log(self.prob(c, token)) for c, token in ng) / len(ng)))
        return result


# This function calls the file frankenstein.txt and creates the n-gram model based on the data recieved from the file
def create_ngram_model(n, path):
    ngram_model = NgramModel(n)
    with open(path, "r+") as file_f:
        [ngram_model.update(line) for line in file_f]

    return ngram_model


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Around 10 hours 
"""

feedback_question_2 = """
Not that challenging. I had to work a little more on the random token and text part but it wasn't bad.
"""

feedback_question_3 = """
I liked the assignment overall. It was kind of different in terms of what we have been doing till now. In my opinion
the assignment was kind of alright, more hints would have certainly helped complete it faster.
"""
