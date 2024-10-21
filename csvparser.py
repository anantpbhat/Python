#!/usr/bin/env python3

import re, argparse

parser = argparse.ArgumentParser(description="Parse line to replace commas with TABs except in double quotes")
parser.add_argument("--input", "-i", metavar='<file-name>', type=str, help="Provide input CSVB file path")
args = parser.parse_args()

with open(args.input, 'r') as csvfl:
    for csvln in csvfl:
        print(re.sub(r'("[^"]+")|,', lambda x: x.group(1) if x.group(1) else x.group().replace(',', '\t'), csvln.rstrip()))
        ###print("New CSV Line: %s" % newln)

