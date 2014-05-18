import csv as csv
import hashlib
from sets import Set

def func_hash(parameter):
    hash_object = hashlib.sha384(parameter)
    table_hash = hash_object.hexdigest()
    return table_hash

def myFunk():
	with open('users.csv', 'w') as fp:
	    a = csv.writer(fp, delimiter=',')
	    roles = ['inspector', 'admin']
	    data = [['Userneme', 'hash_password', 'role'],
	            ['Olya', func_hash('Olya'), 'admin'],
	            ['Stas', func_hash('Stas'), 'admin'],
	            ['Dima', func_hash('Dima'), 'admin'],
	            ['Kyrylo', func_hash('Kyrylo'), 'admin'],
	            ['Lubchyk', func_hash('Lubchyk'), 'inspector'],
	            ['Sashko', func_hash('Sashko'),roles],
	            ]
	    a.writerows(data)

myFunk()