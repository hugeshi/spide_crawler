if __name__ == '__main__':
    import csv

    with open('../../110com.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            print row[0], row[1]
