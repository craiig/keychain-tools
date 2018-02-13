#!/usr/bin/env python
import json
import subprocess
from pprint import pprint
import argparse
import os
from bs4 import BeautifulSoup
import sys
import tempfile
import collections

def load_database(filename):
    #database = {}
    database = collections.OrderedDict()
    if filename and os.path.exists(filename):
        print "loading existing program json"
        try:
            with open(filename) as fh:
                #https://stackoverflow.com/questions/6921699/can-i-get-json-to-load-into-an-ordereddict-in-python
                database = collections.OrderedDict(json.load(fh, object_pairs_hook=collections.OrderedDict))
        except ValueError as e:
            print "error parsing json"
            print e
            database = None

    return database
    
def write_database(db, filename):
    with open(filename, "w+") as out:
        json.dump(db, out, indent=4)

def parse_gcc(db, filename):
    with open(filename) as fh:
        soup = BeautifulSoup(fh, "lxml")

    # for GCC we only include optimizations included in the default
    # optimizations ignoring experimental and elective floating point opts
    # if we wish to include these later, change what gets added to opt_list

    lists = soup.select('dl')
    opt_list = [c for c in lists[1].children]

    all_opts = []
    current_opt = None
    seen_desc = False
    #while len(opt_list) > 0:
    for c in opt_list:
        #c = opt_list.pop(0)
        if c.name == 'dt':
            if current_opt:
                if not seen_desc:
                    current_opt['alternate_names'] = current_opt.get('alternate_names', [])
                    current_opt['alternate_names'].append(c.text)
                else:
                    all_opts.append( current_opt )
                    current_opt = { "name": c.text }
                    seen_desc = False
            else:
                current_opt = { "name": c.text }
                seen_desc = False

        if c.name == 'dd':
            assert current_opt, "saw dd without a dt"
            assert current_opt.get('name', None) != None, "must have opt name"
            assert current_opt.get('description', False) == False, "dont overwrite a previous description"
            seen_desc = True

            current_opt['description'] = c.text.encode('utf-8')

    #insert last element
    if current_opt and seen_desc:
        all_opts.append( current_opt )

    #apply to db
    # TODO tag these optimizations as coming from GCC
    for o in all_opts:
        if not o['name'] in db:
            db[o['name']] = {}
        #else:
            ##ordered dict hack, do a removal and reinsert to establish good order (to fix a badly ordered file)
            ## can remove after this is done once?
            #entry = db[o['name']]
            #del db[o['name']]
            #db[o['name']] = entry

        entry = db[o['name']]
        entry['description'] = o.get('description', None)
        if 'alternate_names' in o:
            entry['alternate_names'] = o['alternate_names']
        entry['origin'] = 'gcc'

    return all_opts

def remove_old_entries(db, new_entries):
    for k,v in db.iteritems():
        if k not in new_entries:
            print "delete {}".format(k)

def manually_tag_opts(db, args):
    # show a vim window with the opt description and a window to add tags
    for name,o in db.iteritems():

        if args.manually_skip_tagged and 'tags' in o and len(o['tags']) > 0:
            print "skipping {}".format(name)
            continue

        tags_fh = tempfile.NamedTemporaryFile(mode="w+", delete=True)
        tags_file = tags_fh.name
        if 'tags' in o:
            tags_fh.write(", ".join(o['tags']))
            tags_fh.flush()

        desc_fh = tempfile.NamedTemporaryFile(mode="w+", delete=True)
        desc_file = desc_fh.name
        if 'description' in o and o['description'] != None:
            desc_fh.write(name)
            desc_fh.write("\n")
            if 'alternate_names' in o:
                desc_fh.write(" ".join(o['alternate_names']))
                desc_fh.write("\n")
            desc_fh.write(o['description'].encode('utf-8'))
            desc_fh.flush()

        #loop in case we make mistakes
        cont = 'r' #repeat by default unless we go next or no
        while cont != 'y':
            # btw vim works only when we aren't redirecting stdin
            cmd_args = ['vim', "survey_questions.md", desc_file, "-O"
                , "+:bot split +:edit {}".format(tags_file)
                , "+:resize 5"
            ]
            subprocess.call(cmd_args)

            tags_fh.seek(0)
            tags = tags_fh.read()
            tags = [s.strip() for s in tags.split(',')]
            o['tags'] = tags
            print "parsed tags for variant {}: {}".format(name, tags)

            cont = raw_input('continue? (y|n|r)')
            if cont == 'n':
                return

            write_database(db, args.db)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='read json files and implement a basic interface to tag each optimization')
    parser.add_argument('--opt_inputs', '-oi', help="a structure list of optimizations")
    parser.add_argument('--db', help="where to store data on the optimizations", required=True)
    parser.add_argument('--gcc_parse', '-g', help='parse gcc html docs and enrich database')
    parser.add_argument('--manually_tag', '-m', help='manually tag the optimizatins with tags', action='store_true')
    parser.add_argument('--manually_skip_tagged', '-mst', help='skip already tagged', action='store_true')

    parser.add_argument('--remove_old_entries', help="remove old entries", action='store_true')

    args = parser.parse_args()

    db = load_database(args.db)

    if args.gcc_parse:
        gcc_entries = parse_gcc(db, args.gcc_parse)

        if args.remove_old_entries:
            new_entries = [e['name'] for e in gcc_entries]
            remove_old_entries(db, new_entries)

    if args.manually_tag:
        manually_tag_opts(db, args)

    write_database(db, args.db)
