#!/usr/bin/env python
import sys, json, re
from pprint import pprint
import difflib
import colorama
colorama.init()

# performs a diff of the salient parts of two hash traces
# to help debug and determine the cause of differences

import argparse
parser = argparse.ArgumentParser(description='Diff two hash traces')
parser.add_argument('left', help="left side trace")
parser.add_argument('right', help="right side trace")
args = parser.parse_args()

left = json.load(open(args.left))
right = json.load(open(args.right))


def diff_string(left, right):
    l = left.splitlines(1)
    r = right.splitlines(1)
    results = difflib.ndiff(l, r)
    #print ''.join( difflib.ndiff(l, r))
    for i in results:
        if i[0] == ' ':
            sys.stdout.write( colorama.Fore.CYAN)
        elif i[0] == '+':
            sys.stdout.write( colorama.Fore.GREEN)
        elif i[0] == '-':
            sys.stdout.write( colorama.Fore.RED)
        elif i[0] == '?':
            sys.stdout.write( colorama.Fore.YELLOW )
        sys.stdout.write(i)
    print colorama.Style.RESET_ALL
    return 

def byte_diff(left, right):
    print colorama.Fore.YELLOW + colorama.Style.BRIGHT +"Byte-by-byte Diff:" + colorama.Style.RESET_ALL
    if len(left) == len(right):
        for i in range(0, len(left)):
            if left[i] == right[i]:
                #print (colorama.Fore.GREEN + left[i]),
                sys.stdout.write( colorama.Fore.GREEN + left[i] )
            else:
                sys.stdout.write (colorama.Fore.YELLOW + "(" 
                        + colorama.Fore.RED + left[i]
                        + colorama.Fore.YELLOW + "|"
                        + colorama.Fore.RED + right[i]
                        + colorama.Fore.YELLOW + ")"
                        )
        print colorama.Style.RESET_ALL
    else:
        print "cannot diff strings, length mismatch"

def print_one(left, right):
    print "left:"
    pprint(left, depth=1)
    print "right:"
    pprint(right, depth=1)

def compare_bytecode(left, right):
    print "comparing bytecode"
    print_one(left, right)
    if left['hash'] != right['hash']:
        print "bytecode hash difference! walking traces"
        ltrace = left['trace']
        rtrace = right['trace']
        for i in range(0, max(len(ltrace), len(rtrace))):
            if i < len(ltrace) and i < len(rtrace):
                #appears on both sides:
                print "comparing both sides"
                if ltrace[i]['localHash'] != rtrace[i]['localHash']:
                    print "mismatch trace:"
                    #print_one(ltrace[i], rtrace[i])
                    diff_string(ltrace[i]['bytecode'], rtrace[i]['bytecode'])
                else:
                    print "matching"
                    #print_one(ltrace[i], rtrace[i])
            elif i < len(ltrace):
                #only on left
                print "only appears on left:"
            elif i < len(rtrace):
                #only on right
                print "only appears on right:"
        #print_one( left['trace'][0], right['trace'][0])
    else:
        print "bytecode hashes equal"

def compare_primitives(left, right):
    print "comparing primitives"
    #print_one(left, right)
    #TODO primitive tracing
    if left['hash'] != right['hash']:
        print "primitive hash difference"
    else:
        print "primitive hashes equal"

def compare_roots(left, right):
    print_one(left, right)
    if left['mergedHash'] != right['mergedHash']:
        print "merged hash difference"
        compare_bytecode(left['bytecode'], right['bytecode'])
        compare_primitives(left['primitives'], right['primitives'])

compare_roots(left, right)
