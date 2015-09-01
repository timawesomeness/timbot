#Shamelessly copied from /u/Gorgyle

from random import randint

cont = 'true'
five = []
seven = []
name1s = []
name2s = []

for line in open('haiku/list5'):
    five.append(line)

for line in open('haiku/list7'):
    seven.append(line);

for line in open('haiku/name1'):
        name1s.append(line);

for line in open('haiku/name2'):
        name2s.append(line);

def create():
    poem1 = five[randint(0,len(five)-1)]
    poem2 = seven[randint(0,len(seven)-1)]
    poem3 = five[randint(0,len(five)-1)]
    poem = poem1 + " " + poem2 + " " + poem3

        #replaces common names with name lists

    if poem.find('Tom') > -1:
        newname = name1s[randint(0,len(name1s)-1)]
        newname = newname.replace('\n','')
        poem1 = poem1.replace('Tom', newname)
        poem2 = poem2.replace('Tom', newname)
        poem3 = poem3.replace('Tom', newname)

    if poem.find('Mary') > -1:
        newname = name2s[randint(0,len(name2s)-1)]
        newname = newname.replace('\n','')
        poem1 = poem1.replace('Mary', newname)
        poem2 = poem2.replace('Mary', newname)
        poem3 = poem3.replace('Mary', newname)

    poem1 = poem1.replace('\n', '')
    poem2 = poem2.replace('\n', '')
    poem3 = poem3.replace('\n', '')

    return poem1, poem2, poem3
