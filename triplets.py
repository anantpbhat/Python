#!/usr/bin/env python3.6

import os

def triplets(a, b, c):
    n = 0
    trip = []
    for j in b:
        for i in a:
            for k in c:
                if j >= i and j >= k:
                    trip.append([])
                    trip[n].append(i)
                    trip[n].append(j)
                    trip[n].append(k)
                    n += 1

    return (len(trip), trip)


if __name__ == '__main__':
###    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    lenaLenbLenc = input().split()
    lena = int(lenaLenbLenc[0])
    lenb = int(lenaLenbLenc[1])
    lenc = int(lenaLenbLenc[2])

    arra = list(map(int, input().rstrip().split()))
    arrb = list(map(int, input().rstrip().split()))
    arrc = list(map(int, input().rstrip().split()))

    (ans, details) = triplets(arra, arrb, arrc)
    print("Total triplets:", ans)
    print("Triplets are:", details)

###  fptr.write(str(ans) + '\n')
###    fptr.close()