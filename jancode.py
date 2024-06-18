import csv
import pickle
import os
from dotenv import load_dotenv   # type: ignore


def getJancode() -> dict:
    jancode = {}
    with open('./{}'.format(os.environ['JANCODE']), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            EANs = row['EAN'].split(',')
            jancode[row['ASIN']] = EANs[0]

    return jancode


def getCodes(acc: str) -> dict:
    with open('./pickle/code_dict_{}.pickle'.format(acc), 'rb') as f:
        code_dict = pickle.load(f)

    return code_dict


def makeCSV(acc: str, code: dict, jancode: dict):

    header = ['code', 'jancode']
    data = []
    for a in code.items():
        data.append([code[a], jancode[a]])

    with open('./csv/{}.csv'.format(acc), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def ftpCSV():
    pass


def main():
    load_dotenv()
    # jancode = getJancode()
    accounts = os.environ['ACCOUNTS']
    accounts = accounts.split(',')

    for acc in accounts:
        code = getCodes(acc)
        makeCSV(acc, code, jancode)


if __name__ == '__main__':
    main()
