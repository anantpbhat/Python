def getin():
   div = int(input("Enter Divident: "))
   dvs = int(input("Enter Divisor: "))
   return (div, dvs)

try:
   (DIV, DVS) = getin()
   print()
   print("Result of dividing", DIV, "by", DVS, "is:", DIV / DVS)

except ZeroDivisionError:
   print("ERROR: Divisor has to be a non-zero number")
