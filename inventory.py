import json
import os
import random
import requests
from passlib.hash import pbkdf2_sha256 as pbk
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from pprint import pprint


ENCODING = 'utf-8'
DB_PATH = os.path.join(os.path.curdir, 'inventory.db')


def scrambleWord(word):
    """Randomize the letters in word and return the resulting string."""
    word_list = list(word)
    random.shuffle(word_list)
    word = ''.join(word_list)
    return word


def generateItems():
    """Generate a dictionary of retail products and store the data in items.json.

    Pulls a list of items and artificially doubles it with scrambled item names.
    Each item is given a random PLU, UPC, and department number.
    Each dictionary key is the item's PLU.
    """
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
        department = (plu % 7) + 1
        print('UPC:{0} | PLU:{1} | Item:{2} | D{3}'.format(upc, plu, item, department))

        if plu in data:
            print('Duplicate found: {}'.format(plu))
            continue

        data[plu] = {'upc':upc, 'department':department, 'model':item}

    with open('items.json', 'w') as f:
        json.dump(data, f)


def generatePO():
    """Create dumby Purchase Orders and store them in pos.json.

    Each PO is asigned one random vendor and department number,
    along with a random length list of items belonging to said department.

    Returns: True if items.json successfully opens, False otherwise.
    """
    try:
        with open('items.json', 'r') as f:
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
        po_dict[po_num] = {'department': (po_num % 7) + 1, 'items': {}, 'vendor': random.choice(vendors)}

    for key in items_dict:
        match_found = False
        loops = 0
        while not match_found:
            loops += 1
            if loops > 200:
                print('\n\nToo many loops.\n\n')
                break
            po, department = random.choice(list(po_dict.items()))
            department = department['department']
            print('PO department: {}'.format(department))
            print('item plu: {} department: {}'.format(key, items_dict[key]['department']))
            if items_dict[key]['department'] == department:
                max_count = random.randint(1, 20)
                po_dict[po]['items'][key] = max_count
                match_found = True

    with open('pos.json', 'w') as f:
        json.dump(po_dict, f)
    return True


def fillDB():
    """Create a database and populate two tables(named items and purchase_order).

    The 'items' and 'purchase_order' tables are populated with the data from items.json
    and pos.json respectively.
    """
    with open('items.json') as f:
        data = json.load(f)

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(DB_PATH)
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
        if query.exec_("insert into items values({}, '{}', '{}', {})".format(key, data[key]['upc'],
                                                                      data[key]['model'], data[key]['department'])):
            print("values({}, {}, {}, {}) successfully inserted.".format(key, data[key]['upc'], data[key]['model'], data[key]['department']))
        else:
            print("values({}, {}, {}, {}) unsuccessfully inserted.".format(key, data[key]['upc'], data[key]['model'], data[key]['department']))
            print(query.lastError().text())

    with open('pos.json') as f:
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
                       .format(key, po_dict[key]['vendor'], po_dict[key]['department'], item_string)):
            print("values({}, {}, {}, {}) successfully inserted."\
                  .format(key, po_dict[key]['vendor'], po_dict[key]['department'], item_string))
        else:
            print("values({}, {}, {}, {}) unsuccessfully inserted."\
                  .format(key, po_dict[key]['vendor'], po_dict[key]['department'], item_blob))
            print(query.lastError().text())


def createEmployeeTable():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(DB_PATH)
    if not db.open():
        print('DB could not be opened')
        error = QSqlDatabase.lastError()
        print(error.text())
        return False
    query = QSqlQuery()
    if not query.exec_("drop table employee"):
        print(query.lastError().text())
    if not query.exec_("create table employee(id int primary key, first_name varchar(10), "\
                "last_name varchar(10), posistion int, pass_hash varchar(200))"):
        print(query.lastError().text())
    if not query.exec_("insert into employee values({}, '{}', '{}', {}, '{}')".\
                format(162973, 'Jon', 'Michie', 2, pbk.hash('Michie'))):
        print(query.lastError().text())
    query.exec_("insert into employee values({}, '{}', '{}', {}, '{}')".\
                format(131901, 'Ben', 'Terry', 3, pbk.hash('Terry')))
    query.exec_("insert into employee values({}, '{}', '{}', {}, '{}')".\
                format(150697, 'Daniel', 'Silva', 2, pbk.hash('Silva')))
    query.exec_("insert into employee values({}, '{}', '{}', {}, '{}')".\
                format(68412, 'James', 'Hutchetson', 2, pbk.hash('Hutchetson')))
    query.exec_("insert into employee values({}, '{}', '{}', {}, '{}')".\
                format(161844, 'MacKenly', 'Gamble', 1, pbk.hash('Gamble')))
    query.exec_("insert into employee values({}, '{}', '{}', {}, '{}')".\
                format(141047, 'George', 'Huston', 1, pbk.hash('Huston')))
    query.exec_("insert into employee values({}, '{}', '{}', {}, '{}')".\
                format(46045, 'Arthur', 'Art', 1, pbk.hash('Art')))


def testHashVerification(name):
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(DB_PATH)
    if not db.open():
        print('DB could not be opened')
        error = QSqlDatabase.lastError()
        print(error.text())
        return False
    query = QSqlQuery()
    if not query.exec_("select pass_hash from employee where last_name = '{}'".format(name)):
        print(query.lastError().text())
    elif not query.next():
        print('Table values not found')
    else:
        pass_hash = query.value(0)

        if pbk.verify(name, pass_hash):
            print('It\'s a match!')
        else:
            print('Match not found.')


if __name__ == '__main__':

    generateItems()
    generatePO()
    fillDB()
    createEmployeeTable()
    testHashVerification('Terry')
