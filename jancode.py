import csv
import pickle
import os
from dotenv import load_dotenv   # type: ignore
from ftplib import FTP
import time

def getJancode() -> dict:
    jancode = {}
    with open('./{}'.format(os.environ['JANCODE']), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            EANs = row['Product Codes: EAN'].split(',')
            jancode[row['ASIN']] = EANs[0]

    return jancode


def getCodes(acc: str) -> dict:
    with open('./pickle/code_dict_{}.pickle'.format(acc), 'rb') as f:
        code_dict = pickle.load(f)

    return code_dict


def makeCSV(acc: str, code: dict, jancode: dict) -> None:

    header = ['code', 'jancode']
    data = []
    for a in code.items():
        data.append([code[a], jancode[a]])

    with open('./csv/{}.csv'.format(acc), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def login_server(acc) -> list:
    PASS1 = os.environ['PASS1']
    PASS2 = os.environ['PASS2']

    PASS = PASS1 if acc not in os.environ['ACC_LIST1'] else PASS2
    if acc in os.environ['ACC_LIST2']:
        acc = acc + "-store"
    acc = "store-{}".format(acc)

    return acc, PASS


def ftpCSV(acc):
    PASS, acc = login_server(acc)
    csv_pass = './csv/'
    try:
        ftp = FTP(os.environ['FTP_ADDRESS'], acc, PASS)
    except BaseException:
        raise Exception('login error')
    
    files = os.listdir(csv_pass)
    for filename in files:
        with open(csv_pass + filename, "rb") as f:
            ftp.storbinary("STOR /" + filename, f)
        time.sleep(60)

def main():
    load_dotenv()
    jancode = getJancode()
    accounts = os.environ['ACCOUNTS']
    accounts = accounts.split(',')

    for acc in accounts:
        code = getCodes(acc)
        makeCSV(acc, code, jancode)
        ftpCSV(acc)



if __name__ == '__main__':
    main()
    
