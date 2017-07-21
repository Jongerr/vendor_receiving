import json
import random
import requests
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from pprint import pprint


ENCODING = 'utf-8'


def scrambleWord(word):

    word_list = list(word)
    random.shuffle(word_list)
    word = ''.join(word_list)
    return word


def generateItems():
    
    response = requests.get('https://www.randomlists.com/data/things.json')
    json_data = response.json()
    items = json_data['RandL']['items']

    #double sample size by scrambling item names
    scrambled_list = []
    for item in items:
        scrambled_item = scrambleWord(item)
        scrambled_list.append(scrambled_item)

    items = items + scrambled_list

    data = {}
    for item in items:
        random.seed(item)
        upc = random.randint(100000000000, 999999999999)
        plu = random.randint(1000, 9999999)
        department = (plu & 7) + 1
        print('UPC:{0} | PLU:{1} | Item:{2} | D{3}'.format(upc, plu, item, department))

        if plu in data:
            print('Duplicate found: {}'.format(plu))
            continue

        data[plu] = {'UPC':upc, 'Department':department, 'Model':item}

    with open('items.txt', 'w') as f:
        json.dump(data, f)


def generatePO(filename):

    try:
        with open(filename, 'r') as f:
            items_dict = json.load(f)
    except FileNotFoundError:
        return False
    
    vendors = ['Dyson', 'Ingrammicro', 'LKG', 'Inland', 'Sandisk', 'Seagate', 'Hasbro', 'Mattel',\
               'Gear Head', 'Logitech', 'NTE', 'Dell', 'Microsoft', 'Right Stuff', 'Alliance', 'Energizer']

    po_dict = {}
    for i in range(50):
        po_num = 24000000 + random.randint(1, 999999)
        if po_num in po_dict:
            continue
        po_dict[po_num] = {'department': (po_num % 7) + 1, 'items': [], 'vendor': random.choice(vendors)}

    for key in items_dict:
        match_found = False
        while not match_found:
            po, department = random.choice(list(po_dict.items()))
            department = department['department']
            if items_dict[key]['Department'] == department:
                max_count = random.randint(1, 20)
                po_dict[po]['items'].append((key, max_count))
                match_found = True

    with open('pos.txt', 'w') as f:
        json.dump(po_dict, f)
    return True


def filldb():

    with open('items.txt') as f:
        data = json.load(f)

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('C:\\receiving_project\\vendor_receiving\\inventory.db')
    if not db.open():
        print('DB could not be opened')
        error = QSqlDatabase.lastError()
        print(error.text())
        return False

    query = QSqlQuery()
    if query.exec_("drop table items"):
        print('successfully dropped table')
    else:
        print('unsuccessfully dropped table')
        print(query.lastError().text())
    if query.exec_("create table items(plu int primary key, upc varchar(12) unique, "
                "model varchar(20), department int)"):
        print('success')
    else:
        print('failure')
        print(query.lastError().text())
    for key in data:
        if query.exec_("insert into items values({}, '{}', '{}', {})".format(key, data[key]['UPC'],
                                                                      data[key]['Model'], data[key]['Department'])):
            print("values({}, {}, {}, {}) successfully inserted.".format(key, data[key]['UPC'], data[key]['Model'], data[key]['Department']))
        else:
            print("values({}, {}, {}, {}) unsuccessfully inserted.".format(key, data[key]['UPC'], data[key]['Model'], data[key]['Department']))
            print(query.lastError().text())

    with open('pos.txt') as f:
        po_dict = json.load(f)

    if query.exec_("drop table purchase_order"):
        print('successfully dropped table')
    else:
        print('unsuccessfully dropped table')
        print(query.lastError().text())
    if query.exec_("create table purchase_order(po int primary key, vendor varchar(30), "
                   "department int, items blob)"):
        print('success')
    else:
        print('failure')
        print(query.lastError().text())
    for key in po_dict:
        item_string = json.dumps(po_dict[key]['items'])
        item_blob = item_string.encode(ENCODING)
        if query.exec_("insert into purchase_order values({}, '{}', {}, '{}')"\
                       .format(key, po_dict[key]['vendor'], po_dict[key]['department'], memoryview(item_blob))):
            print("values({}, {}, {}, {}) successfully inserted."\
                  .format(key, po_dict[key]['vendor'], po_dict[key]['department'], item_string))
        else:
##            print("values({}, {}, {}, {}) unsuccessfully inserted."\
##                  .format(key, po_dict[key]['vendor'], po_dict[key]['department'], item_blob))
            print(query.lastError().text())
                                                                            


if __name__ == '__main__':

    #generateItems()
    filldb()
    #generatePO('items.txt')
