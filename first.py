import argparse

parser = argparse.ArgumentParser(description="Print Divisible Numbers")
parser.add_argument("-dv", type=int, metavar='', required=True, help="Specify Divisor")
parser.add_argument("-rg", type=int, metavar='', required=True, help="Specify range of numbers to try")
args = parser.parse_args()

def div(dv, rg):
    for i in range(rg):
        if (i % dv) == 0:
            print(i)
        else:
            print(i, "is not a multiple of", dv)

div(args.dv, args.rg)
