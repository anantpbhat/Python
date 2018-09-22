import argparse

parser = argparse.ArgumentParser(description="Print Divisible / Odd Numbers")
parser.add_argument("-dv", type=int, metavar='', required=False, help="Specify Divisor")
parser.add_argument("-rg", type=int, metavar='', required=True, help="Specify range of numbers to try")
parser.add_argument("-od", action="store_true", help="List Odd numbers from specified range")
args = parser.parse_args()

def div(dv, rg):
    divlist = [ i for i in range(rg) if (i % dv) == 0 ]
    print("Following numbers till {} that's divisible by {} are: {}".format(rg - 1, dv, divlist))

def Odd(rg):
    odlist = [ i for i in range(rg) if ( i % 2) == 1 ]
    print("Odd numbers list till {} are: {}".format(rg -1, odlist))

if args.dv:
    div(args.dv, (args.rg + 1))
    exit(0)
elif args.od:
    Odd(args.rg + 1)
    exit(0)
else:
    print("One of the two arguments -dv or -od is required. Exiting...")
    exit(1)

