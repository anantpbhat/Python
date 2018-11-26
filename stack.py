#!/usr/bin/env python3.6


class Actions():
    def __init__(self):
        self.T = input("Enter total items: ")
        self.lst = input("Enter " + self.T + " items: ").split()

    def addall(self):
        sum = 0
        for i in self.lst:
            sum += int(i)
        return sum

    def avg(self):
        l = len(self.lst)
        S = items.addall()
        avrg = S / l
        return avrg

    def pushin(self):
        x = int(input("Enter new item: "))
        self.lst.append(x)

    def popout(self):
        del self.lst[-1]


if __name__ == "__main__":
    items = Actions()
    print("Sum of all items:", items.addall())
    print("Average of items in the List:", items.avg())
    items.pushin()
    print("List of Current Items: {}".format(items.lst))
    items.popout()
    print("List of Items after last removal: {}".format(items.lst))
