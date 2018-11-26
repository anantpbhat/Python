#!/usr/bin/env python3.6

import re

class RegEx():
    def __init__(self):
        self.yp = re.compile(r'^y$|^yes$', re.I)
        self.np = re.compile(r'^n$|^no$', re.I)
        self.qp = re.compile(r'^q$|^quit$', re.I)

class Items():
    def __init__(self):
        self.items = {"Soccer Ball": 9, "Rice": 3, "Python Book": 30, "Apples": 2, "Printer": 150}
        self.itm = input("Enter Item you want to buy: ")

    def check_item(self):
        if self.itm not in self.items:
            print("Invalid, we don't sell this Item!")
            self.itm = input("Enter Item to buy or (Q|q) to quit: ")
            if regx.qp.search(self.itm):
                return
            Items.check_item(self)
        else:
            return

    def get_price(self, vlditm):
        self.vlditm = vlditm
        self.itmpr = self.items[self.vlditm]

class Cust():
    def __init__(self):
        print("Welcome to our Store!!!")
        self.ans1 = input("Are you a Student (y/n)? ")
        self.ans2 = input("Have you shopped with us at least 3 times or more (y/n)? ")

    def checkcust(self):
        if regx.yp.search(self.ans1) and regx.np.search(self.ans2):
            self.custtyp = "Student "
            self.dis = 0.05
        elif regx.np.search(self.ans1) and regx.yp.search(self.ans2):
            self.custtyp = "Loyal "
            self.dis = 0.10
        elif regx.yp.search(self.ans1) and regx.yp.search(self.ans2):
            self.custtyp = "Loyal Student "
            self.dis = 0.15
        else:
            self.custtyp = ""
            self.dis = 0

    def nextcust(self):
        self.ansl = input("\nNext Customer (y/n)? ")
        if regx.qp.search(self.ansl) or regx.np.search(self.ansl):
            return "BR"


if __name__ == "__main__":
    regx = RegEx()
    while True:
        cust = Cust()
        cust.checkcust()
        print("Welcome {}Customer".format(cust.custtyp))
        item = Items()
        item.check_item()
        if not regx.qp.search(item.itm):
            item.get_price(item.itm)
            finalprice = item.itmpr - (item.itmpr * cust.dis)
            print("Customer Price for {} is: {}".format(item.itm, finalprice))
        if cust.nextcust() == "BR":
            break
        print("")

    print("Quiting at users request...")
    exit(code=0)
