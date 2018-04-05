#!/usr/bin/env python

# check for regressions between two versions of resilience_outcome.json
# look for changes in the tests, which compilers are tested, and if a test
# is passing.
#
# used to make sure changes we make for compatibility aren' unknowingly t
# affecting code correctness

import argparse
import json
import colorama as c
c.init()
from pprint import pprint

def diff_sets(old, new, thing_name):
    in_old_not_new = old.difference(new)
    in_new_not_old = new.difference(old)
    if len(in_old_not_new):
        print c.Fore.RED + thing_name + " deleted:"
        print list(in_old_not_new)
        print c.Style.RESET_ALL
    if len(in_new_not_old):
        print c.Fore.GREEN + thing_name + " added:"
        print list(in_new_not_old)
        print c.Style.RESET_ALL,

    return len(in_old_not_new) == 0 and len(in_new_not_old) == 0

def diff_outcomes(old, new, print_diff):
    #1. check for changes in tests performed
    #2. check for changes in whether tests pass: full, partial (change in # of unique), failure
    assert 'programs' in old
    assert 'programs' in new

    old_names = set([p['name'] for p in old['programs']])
    new_names = set([p['name'] for p in new['programs']])

    diff_sets(old_names, new_names, 'Tests')

    # check that for differences in outcome for each test
    old_programs = {p['name']:p for p in old['programs']}
    new_programs = {p['name']:p for p in new['programs']}

    for old_name,old_p in old_programs.iteritems():
        print "checking {}".format(old_name)

        new_p = new_programs.get(old_name, None)
        if not new_p:
            # we already listed the deleted tests so we don't need to list here
            print c.Fore.RED + "Old test not found in new tests: {}".format(old_name)
            print c.Style.RESET_ALL,
            continue

        old_compilers = set([comp for comp in old_p['program_hashes']])
        new_compilers = set([comp for comp in new_p['program_hashes']])

        diff_sets(old_compilers, new_compilers, "Compilers used in {}".format(old_name))

        for old_c,old_hashes in old_p['program_hashes'].iteritems():
            #print old_c
            #count old unique, count new unique
            new_hashes = new_p['program_hashes'].get(old_c, None)
            if not new_hashes:
                print c.Fore.RED + "Compiler {} not found in tests: {}".format(old_c, old_name)
                print c.Style.RESET_ALL,
                continue

            old_unique = len(set( old_hashes ))
            new_unique = len(set( new_hashes ))
            #print "Old Unique Hashes: {} New Unique Hashes: {}".format(old_unique, new_unique)
            if old_unique != new_unique:
                if old_unique < new_unique:
                    print c.Fore.RED + "*** Greater number of unique hashes in tests {} for compiler {}".format(old_name, old_c)
                if old_unique > new_unique:
                    print c.Fore.GREEN + "*** Lower number of unique hashes in tests {} for compiler {}".format(old_name, old_c)
                print "Old Unique Hashes: {} New Unique Hashes: {}".format(old_unique, new_unique)

                if print_diff:
                    #pprint(old_hashes)
                    print c.Fore.RED,
                    pprint(old_p)
                    print c.Fore.GREEN,
                    #pprint(new_hashes)
                    pprint(new_p)
                print c.Style.RESET_ALL,

def main():
    parser = argparse.ArgumentParser(description='run resilience test using input')
    parser.add_argument('--old', '-o', help='old resilience outcome to compare against', required=True)
    parser.add_argument('--new', '-n', help='new resilience outcome to check', required=True)
    parser.add_argument('--diff', '-d', help='enable to print out program diff', action='store_true')
    args = parser.parse_args()

    with open(args.old) as fh:
        old = json.load(fh)

    with open(args.new) as fh:
        new = json.load(fh)

    diff_outcomes(old, new, args.diff)

if __name__ == "__main__":
    main()
