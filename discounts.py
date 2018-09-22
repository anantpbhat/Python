
import re

def quitnow(x):
    if x == "quit":
        print("Quiting at users request...")
        exit(0)
    exit(1)

def ifstudent(x, y):
    ins = input("Are you a Student (y/n/q): ")
    if qy.search(ins):
        x += 0.1
        y = " Student"
        return x, y
    elif qn.search(ins):
        return x, y
    elif qp.search(ins):
        quitnow("quit")
    else:
        print("That's an invalid input. Quiting...")
        quitnow("BAD")

def ifloyal(a, b):
    inl = input("Have you shopped with us for atleast 5 times or more (y/n/q)? ")
    if qy.search(inl):
        a += 0.05
        b = " Loyal" + b
        return a, b
    elif qn.search(inl):
        return a, b
    elif qp.search(inl):
        quitnow("quit")
    else:
        print("Invalid input...", "\n")
        b = "Invalid"
        return a, b

def getitem():
    ui = input("Enter an item to purchase or (q/Q) to quit: ")
    if ui.title() in avlitems:
        return ui.title()
    elif qp.search(ui):
        quitnow("quit")
    else:
        print("We don't sell this item!!!", "\n")
        return "invalid item"

avlitems = {"Soccer Ball": 9, "Rice": 3, "Python Book": 30, "Apples": 2, "Printer": 150}
qp = re.compile(r'^(q|quit)$', re.I)
qy = re.compile(r'^(y|yes)$', re.I)
qn = re.compile(r'^(n|no)$', re.I)

dis = 0
dis, mesg = ifstudent(dis, "")
dis, mesg = ifloyal(dis, mesg)
while mesg.startswith("Invalid"):
    dis, mesg = ifloyal(dis, "")
print("\n", "Welcome" + mesg + " Customer!!!")

while True:
    itm = getitem()
    if itm.startswith("invalid"):
        continue
    itmprc = avlitems[itm]
    newprc = itmprc - (itmprc * dis)
    print("Price for '{}' item is: {} USD".format(itm, newprc), "\n")
