import os
fhandle = open('stocklist', 'r').read().split('\n')
handle = []
for x in fhandle:
    if not x in handle:
        handle.append(x)
os.remove('stocklist')
newhandle = open('stocklist', 'w+')
for y in handle:
    newhandle.write(y + '\n')