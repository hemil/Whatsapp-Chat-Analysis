import sys
import re
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

__author__ = "hemil"

usage = """Usage: python wordcloud_pm.py "Dead Pool" "Gommora Thanos" crossover_chats.txt | pbcopy
pbcopy will put the output of this code to your clipboard.
Go to wordart.com, import words, paste it in the textbox. Click ok and then visualize.
Voila!
Wordcloud is ready.
"""

stop_words = set(stopwords.words('english'))
stemmer = LancasterStemmer()

try:
    user_one = sys.argv[1]
    user_two = sys.argv[2]
    chat_file_name = sys.argv[3]
except IndexError:
    print usage
    exit(1)

word_count = {}

count = 0


def populate_analysis_dict(chat_line, user, analysis_dict, count):
    if user in chat_line:
        chat_split = chat_line.split(":", 3)
        words = filter(None, re.split("[, \-!?:.'\"]+", chat_split[-1]))
        # Remove Common words
        words = [i for i in words if i not in stop_words]
        for word in words:
            word = unicode(word).encode("utf-8", "ignore").strip().lower()
            try:
                # reduce words to their roots
                word = stemmer.stem(stemmer)
            except:
                pass

            if word in ["<media", "ommited>"]:      # remove emojis and unknown media messages
                return

            if word not in analysis_dict:
                analysis_dict[word] = 1
                count += 1
            else:
                analysis_dict[word] += 1
                count += 1

with open(chat_file_name, "r") as chat_file:
    chats = chat_file.readlines()
    for chat_line in chats:
        chat_line = chat_line.decode("utf-8", "ignore")
        if user_one in chat_line:
            populate_analysis_dict(chat_line, user_one, word_count, count)

for word, count in word_count.iteritems():
    if len(word) <= 4:
        continue
    try:
        print "{word};{count}".format(word=word, count=count)
    except UnicodeDecodeError:
        continue

