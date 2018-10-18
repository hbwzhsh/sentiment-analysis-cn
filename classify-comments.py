import csv

filename = "reviews-20180805-full.csv"
path = "data/"
positive_comments = list()
negative_comments = list()
neutral_comments = list()

with open(path + filename, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Remove empty lines
    lines = list(line for line in csv_reader if line)
    for line in lines:
        comment = line[2]
        ratings = int(line[3])
        if ratings < 30:
            negative_comments.append(comment)
        elif ratings > 30:
            positive_comments.append(comment)
        else:
            neutral_comments.append(comment)

print("Pos count: " + str(len(positive_comments)))
print("Neg count: " + str(len(negative_comments)))
print("Neu count: " + str(len(neutral_comments)))
