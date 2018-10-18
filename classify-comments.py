import csv
import re


def cleanhtml(raw_html):
    regs = ["&nbsp;", "<.*?>", "[\U00010000-\U0010ffff]"]
    clean_text = raw_html
    for reg in regs:
        cleaner = re.compile(reg)
        clean_text = re.sub(cleaner, '', clean_text)
    return clean_text

filename = "reviews-20180805-full.csv"
path = "data/"
positive_comments = list()
negative_comments = list()

with open(path + filename, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Remove empty lines
    lines = list(line for line in csv_reader if line)
    for line in lines:
        comment = line[2]
        ratings = int(line[3])
        if ratings <= 30:
            negative_comments.append(comment)
        elif ratings > 30:
            positive_comments.append(comment)

print("Pos count: " + str(len(positive_comments)))
print("Neg count: " + str(len(negative_comments)))

with open(path + 'positive.txt', 'w', encoding='utf-8') as file:
    for line in positive_comments:
        file.write(cleanhtml(line) + '\n')

with open(path + 'negative.txt', 'w', encoding='utf-8') as file:
    for line in negative_comments:
        file.write(cleanhtml(line) + '\n')


