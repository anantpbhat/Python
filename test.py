import re

def getprice(x):
    if x in cmdty:
        print("Price for item '{}' is: {} USD".format(x, cmdty[x]), "\n")
    else:
        print("{} is not a valid item".format(x), "\n")

cmdty = {"Soccer Ball": 9, "Rice": 3, "Python Book": 30, "Apples": 2, "Printer": 150}
qp = re.compile(r'^(q|quit)$', re.I)

while True:
    ui = input("Enter a Commodity Name: ")
    if qp.search(ui):
        print("Quiting at users request...")
        break
    else:
        getprice(ui.title())
        continue
exit(0)
