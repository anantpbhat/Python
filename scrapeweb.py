#!/usr/bin/env /usr/bin/python3.6

########################################################################
#                                                                      #
# Parse HTML Page, takes input file as an argument or will prompt      #
# for User input.                                                      #
# Author: Anant Bhat.                                                  #
#                                                                      #
# Please capture all version changes below                             #
# Version 1.0 - Initial creation, Anant, 12/02/2018                    #
########################################################################

from bs4 import BeautifulSoup
import requests

with open("/home/abhat/Documents/HTMLs/HomePage.html") as homepg:
    bsoup = BeautifulSoup(homepg, 'lxml')

for fltr in bsoup.find_all('section'):
    print(fltr.h2.text, "-")
    for lst in fltr.find_all('li'):
        print(lst.text + ":", end="\t")
        url = (lst.a)["href"]
        print(url)
    print()
