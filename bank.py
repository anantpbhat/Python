#!/usr/bin/env python3

class Account():
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def __repr__(self):
        return f"Owner Name: {self.owner}, Balance Amount: {self.balance}"

    def deposit(self, dep):
        self.balance = self.balance + dep
        return f"New Balance for {self.owner}: {self.balance}"

    def withdraw(self, draw):
        if self.balance > draw:
            self.balance = self.balance - draw
            return f"New Balance for {self.owner}: {self.balance}"
        else:
            return "Incorrect Withdrawal amount!"


if __name__ == "__main__":
    acct1 = Account("Andy", 200)
    print(acct1.owner)
    print(acct1.balance)
    print(acct1.withdraw(190))
    print(acct1.deposit(50))
    print(acct1)



