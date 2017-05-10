import sys

__author__ = "hemil"


user_one = sys.argv[1]
user_two = sys.argv[2]
chat_file_name = sys.argv[3]

usage = """
Usage: python hourly_pm.py "Dead Pool" "Gommora Thanos" crossover_chats.txt
The code will generate a csv, which can then be used to create comparitive graphs and charts.
"""

try:
    user_one = sys.argv[1]
    user_two = sys.argv[2]
    chat_file_name = sys.argv[3]
except IndexError:
    print usage
    exit(1)


analysis_dict_one = {}
analysis_dict_two = {}


def populate_analysis_dict(chat_line, user, analysis_dict):
    if user in chat_line:
        chat_split = chat_line.split(" ", 1)
        try:
            user_name = chat_line.split(" - ", 1)[1].split(":", 1)[0].encode('utf-8').strip()
        except IndexError:
            return
        false_positives = ["changed the subject", " added ", "security code changed", " left", "changed to",
                           "changed from",
                           "deleted this group's icon", "changed this group's icon", "6 Mar 2017"]
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


with open(chat_file_name, "r") as chat_file:
    chats = chat_file.readlines()
    for chat_line in chats:
        chat_line = chat_line.decode('utf-8', 'ignore')
        populate_analysis_dict(chat_line, user_one, analysis_dict_one)
        populate_analysis_dict(chat_line, user_two, analysis_dict_two)

# generate csv
with open("hourly_chat_analysis_{user_one}_{user_two}.csv".format(user_one=user_one, user_two=user_two), "w+") as f:
    f.write("Time,{user_one},Time,{user_two}\n".format(user_one=user_one, user_two=user_two))
    for day_night in ["AM", "PM"]:
        for hour in xrange(1, 13):
            key = (str(hour) + day_night).strip()
            value_one = str(analysis_dict_one.get(user_one).get(key, 0)).strip()
            value_two = str(analysis_dict_two.get(user_two).get(key, 0)).strip()
            f.write(key + "," + value_one + "," + key + "," + value_two + "\n")
