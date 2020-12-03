############################################################
# CMPSC442: Homework_4
############################################################

# student_name = "Varun Jani"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import os
from math import log, exp
# from queue import PriorityQueue


############################################################
# Section 1: Spam Filter
############################################################

# Function to read the emails once the path is specified, and it extracts the tokens and returns it as a list
def load_tokens(email_path):
    # To open the file using the specified path
    file_obj = open(email_path, encoding="utf8")
    message = email.message_from_file(file_obj)
    token_list = []

    for line in email.iterators.body_line_iterator(message):
        token_list += line.split()

    # Simply close the file
    file_obj.close()
    return token_list


# Function to return a dictionary from the words contained in the email to their Laplace-smoothed probabilities
def log_probs(email_paths, smoothing):
    p_dict = {}

    # For loop to check the path of the email iterating over the paths
    for e in email_paths:
        values = load_tokens(e)

        # From the values, we are looking for a word specifically using for loop
        for x in values:

            # To check if the word is in the dictionary or not
            if x in p_dict:
                p_dict[x] += 1
            else:
                p_dict[x] = 1

    final = sum(p_dict.values())

    # To check the word and its frequency in the dictionary using for loop and items() for dictionary
    for term, w in p_dict.items():
        temp = final + smoothing * (len(p_dict) + 1)
        p_dict[term] = log((w + smoothing) / temp)

    p_dict.update({'<UNK>': log(smoothing / (final + smoothing * (len(p_dict) + 1)))})
    return p_dict


class SpamFilter(object):

    # Simple init function create two log probability dictionaries
    def __init__(self, spam_dir, ham_dir, smoothing):
        spam_path, ham_path = [], []

        # Using os.walk to access the file information
        for dir_path, dir_name, file_name in os.walk(spam_dir):
            spam_path = [dir_path + '/' + f for f in file_name]
        for dir_path, dir_name, file_name in os.walk(ham_dir):
            ham_path = [dir_path + '/' + f for f in file_name]

        self.spam_prob = log_probs(spam_path, smoothing)
        self.ham_prob = log_probs(ham_path, smoothing)

        total_len = len(spam_path) + len(ham_path)

        self.p_ham = log(len(ham_path) / total_len)
        self.p_spam = log(1 - self.p_ham)

    # Function to return whether the email in the given file path is spam or not (returns True or False)
    def is_spam(self, email_path):
        spam_p, ham_p = self.p_spam, self.p_ham
        dict_words = {}

        # Check for the word in the given file, which is accessed using load_tokens function
        for w in load_tokens(email_path):
            if w in dict_words:
                dict_words[w] += 1
            else:
                dict_words[w] = 1

        # Update the ham and spam accordingly after iterating through the dictionary
        for w, count in dict_words.items():

            # To check if the word is in there or not (for spam and ham)
            if w in self.ham_prob:
                ham_p += self.ham_prob[w]
            else:
                ham_p += self.ham_prob["<UNK>"]
            if w in self.spam_prob:
                spam_p += self.spam_prob[w]
            else:
                spam_p += self.spam_prob["<UNK>"]

        # I started these valued with the calculated value and not zero
        if spam_p > ham_p:
            return True
        return False

    # Next two function return the n most indicative words for each category sorted in descending order

    def most_indicative_spam(self, n):
        v = set(self.spam_prob.keys()) & set(self.ham_prob.keys())
        spam_res = {i: log(exp(self.spam_prob[i]) / (exp(self.ham_prob[i]) +
                                                     exp(self.spam_prob[i]))) for i in v}
        ans = sorted([(i, spam_res[i]) for i in spam_res], key=lambda x: x[1], reverse=True)
        return [i[0] for i in ans[:n]]

    def most_indicative_ham(self, n):
        v = set(self.spam_prob.keys()) & set(self.ham_prob.keys())
        ham_res = {i: log(exp(self.ham_prob[i]) / (exp(self.spam_prob[i]) +
                                                   exp(self.ham_prob[i]))) for i in v}
        ans = sorted([(i, ham_res[i]) for i in ham_res], key=lambda x: x[1], reverse=True)
        return [i[0] for i in ans[:n]]


# P.S: I used priority queue also to implement the two most indicative function here. It was slightly slower than the
# sorting method so I decided not to use it. Based on my test cases, this is a faster method. I hope I am not wrong.
# I would love to change it if it isn't because the auto-grader test cases might be different and so I cannot
# be completely sure.

# Best time overall using unittest should be in the range 3.5 to 4.0 seconds

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Around 8-9 hours mainly because of last timing part
"""

feedback_question_2 = """
The second function was challenging at first, and the most indicative part was a whole lot time consuming for me 
because of the time issue. I had to solve a lot of issues there. Please look at the P.S. above, as I have a better
solution if the current one isn't satisfactory. Overall otherwise I had not many stumbling blocks.
"""

feedback_question_3 = """
Assignment was alright. It was a good assignment and helped me learn something new. 
"""
