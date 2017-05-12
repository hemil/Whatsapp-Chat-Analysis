import sys
from itertools import chain, izip, repeat, islice

__author__ = "hemil"

usage = """
Usage: python hourly_group.py avengers_chat.txt,avengers_chat_civil_war.txt
Will give you the number of messages each user has sent in each hour. Will show how the Civil War played out.
"""

try:
    file_names = sys.argv[1].split(",")
except IndexError:
    print usage
    exit(1)

analysis_dict = {}
failed_count = 0


def intersperse(delimiter, seq):
    return islice(chain.from_iterable(izip(repeat(delimiter), seq)), 1, None)


def populate_analysis_dict(chat_line, analysis_dict):
    if ":" not in chat_line:
        return
    chat_split = chat_line.split(" ", 1)
    user_name = chat_line.split(" - ", 1)[1].split(":", 1)[0].encode('utf-8').strip()
    false_positives = ["changed the subject", "added", "security code changed", " left", "changed to", "changed from",
                       "this group's icon", "6 Mar 2017", "removed", "end-to-end encryption"]
    if any(false_positive in chat_line for false_positive in false_positives):
        return
    # date = chat_split[0]
    time = chat_split[1].split("-", 1)[0]
    hour = time.split(":", 1)[0]
    am_pm = time.split(" ", 1)[1]

    hourly_key = (hour + am_pm).strip()
    if user_name not in analysis_dict:
        analysis_dict[user_name] = {}
    else:
        if hourly_key not in analysis_dict[user_name]:
            analysis_dict[user_name][hourly_key] = 0
        else:
            analysis_dict[user_name][hourly_key] += 1

for file_name in file_names:
    with open(file_name, "r") as chat_file:
        chats = chat_file.readlines()
        for chat_line in chats:
            chat_line = chat_line.decode('utf-8', 'ignore')
            try:
                populate_analysis_dict(chat_line, analysis_dict)
            except IndexError:
                failed_count += 1

# generate csv
users = analysis_dict.keys()
headers = [val for val in users for _ in (0, 1)]

with open("hourly_analysis_of_{file_name}.csv".format(file_name=file_names), "w+") as f:
    f.write(",".join(headers) + "\n")
    for day_night in ["AM", "PM"]:
        for i in xrange(1, 13):
            key = (str(i) + day_night).strip()
            values = []
            for user in users:
                value_one = str(analysis_dict.get(user).get(key, 0)).strip()
                values.append(key + "," + value_one)
            f.write(",".join(values) + "\n")

print "Ignored: {count} messages due to missing data sanitization.".format(count=failed_count)
