#!/usr/bin/env python
import json
import subprocess
from pprint import pprint
import argparse
import os
from bs4 import BeautifulSoup
import sys
import tempfile

def load_database(filename):
    database = {}
    if filename and os.path.exists(filename):
        print "loading existing program json"
        try:
            with open(filename) as fh:
                database = json.load(fh)
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

    lists = soup.select('dl')
    opt_list = [c for c in lists[1].children]

    all_opts = []
    current_opt = None
    while len(opt_list) > 0:
        c = opt_list.pop(0)
        if c.name == 'dt':
            if current_opt:
                if not seen_desc:
                    current_opt['alternate_names'] = current_opt.get('alternate_names', [])
                    current_opt['alternate_names'].append(c.string)
                else:
                    all_opts.append( current_opt )
                    current_opt = { "name": c.text }
            else:
                current_opt = { "name": c.text }

        if c.name == 'dd':
            assert current_opt, "saw dd without a dt"
            assert current_opt.get('name', None) != None, "must have opt name"
            assert current_opt.get('description', False) == False, "dont overwrite a previous description"
            seen_desc = True

            current_opt['description'] = c.text

    #apply to db
    for o in all_opts:
        if not o['name'] in db:
            db[o['name']] = {}

        entry = db[o['name']]
        entry['description'] = o.get('description', None)

def manually_tag_opts(db, args):
    # show a vim window with the opt description and a window to add tags
    for name,o in db.iteritems():

        tags_fh = tempfile.NamedTemporaryFile(mode="w+", delete=True)
        tags_file = tags_fh.name
        if 'tags' in o:
            tags_fh.write(", ".join(o['tags']))
            tags_fh.flush()

        desc_fh = tempfile.NamedTemporaryFile(mode="w+", delete=True)
        desc_file = desc_fh.name
        if 'description' in o:
            desc_fh.write(name)
            desc_fh.write("\n")
            desc_fh.write(o['description'])
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
    args = parser.parse_args()

    db = load_database(args.db)

    if args.gcc_parse:
        parse_gcc(db, args.gcc_parse)

    if args.manually_tag:
        manually_tag_opts(db, args)

    write_database(db, args.db)
