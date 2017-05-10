import sys
import re
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

__author__ = "hemil"

usage = """Usage: python wordcloud_group.py "avengers_chats_9_may.txt,avengers_chats_28_dec.txt" | pbcopy
pbcopy will put the output of this code to your clipboard.
The Multiple files support is due to whatsapp's 40k chat limit on emails due to size. This is in case of past backups.
Go to wordart.com, import words, paste it in the textbox. Click ok and then visualize.
Voila!
Wordcloud is ready.
"""

try:
    chat_files_list = sys.argv[1].split(",")
except IndexError:
    print usage
    exit(1)

stop_words = set(stopwords.words('english'))
stemmer = LancasterStemmer()

word_count = {}


def populate_analysis_dict(chat_line, analysis_dict):
    chat_split = chat_line.split(":", 3)
    words = filter(None, re.split("[, \-!?:.'\"]+", chat_split[-1]))
    words = [i for i in words if i not in stop_words]
    for word in words:
        word = unicode(word).encode("utf-8", "ignore").strip().lower()

        try:
            word = stemmer.stem(stemmer)
        except:
            pass

        if word in ["<media","ommited>"]:
            return

        if word not in analysis_dict:
            analysis_dict[word] = 1
        else:
            analysis_dict[word] += 1


def print_word_cloud_content(file_name):
    with open(file_name, "r") as chat_file:
        chats = chat_file.readlines()
        for chat_line in chats:
            chat_line = chat_line.decode("utf-8", "ignore")
            populate_analysis_dict(chat_line, word_count)

    for word, count in word_count.iteritems():
        if len(word) <= 4:
            continue
        try:
            print "{word};{count}".format(word=word, count=count)
        except UnicodeDecodeError:
            continue

for chat_file_name in chat_files_list:
    print_word_cloud_content(chat_file_name)
