import re

qp = re.compile(r'^q$|^quit$', re.I)

### Commit this comment in GITHub to new branch Anant
while True:
    IN = input("Type in some Alphabets or (q|Q) to quit: ")
    if qp.search(IN):
        break
    IN = IN.split()
    for i in IN:
        if not i.isalpha():
            print ("I noticed a non-alphabet character!!!")
            break
