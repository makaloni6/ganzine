import csv
from account import acc

def setJancode(acc):
    with open('./csv/{}.csv'.format(acc), 'r') as f:
        reader = csv.DictReader(f)


def makeCSV():
    pass

def ftpCSV():
    pass

def main():
    pass