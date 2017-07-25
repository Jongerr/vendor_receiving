import json
import random
import requests
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from pprint import pprint


ENCODING = 'utf-8'


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

        data[plu] = {'UPC':upc, 'Department':department, 'Model':item}

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
        po_dict[po_num] = {'department': (po_num % 7) + 1, 'items': [], 'vendor': random.choice(vendors)}

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
            print('item plue: {} department: {}'.format(key, items_dict[key]['Department']))
            if items_dict[key]['Department'] == department:
                max_count = random.randint(1, 20)
                po_dict[po]['items'].append((key, max_count))
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
                       .format(key, po_dict[key]['vendor'], po_dict[key]['department'], memoryview(item_blob))):
            print("values({}, {}, {}, {}) successfully inserted."\
                  .format(key, po_dict[key]['vendor'], po_dict[key]['department'], item_string))
        else:
            print("values({}, {}, {}, {}) unsuccessfully inserted."\
                  .format(key, po_dict[key]['vendor'], po_dict[key]['department'], item_blob))
            print(query.lastError().text())                                                                            


if __name__ == '__main__':

    generateItems()
    generatePO()
    fillDB()
