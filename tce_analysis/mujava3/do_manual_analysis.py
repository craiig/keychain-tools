#!/usr/bin/python
# basic script to parse the manually verified equivalent mutants and extract
# them from the generated mutants

import sys
import tempfile
import argparse
import re
import json
import subprocess
import os
import difflib
from pprint import pprint

def parse_programs(file_handle):
    programs = []
    current_program = None
    #parse states
    EXPECT_TBODY = "EXPECT_TBODY"
    EXPECT_MUTANT_TYPE = "EXPECT_MUTANT_TYPE"

    for l in file_handle:
        header = "<!-- \* (.+?) -->" 
        m = re.search(header, l)
        if m:
            benchmark, = m.groups()
            if current_program:
                programs.append(current_program)

            current_program = {
                "benchmark": benchmark, 
                "equivalent_mutants": []
            }
            #print "new_program: {}".format(current_program)
            #empty list to hold each equiv variant
            parse_state = EXPECT_TBODY

        if current_program is not None:
            if parse_state == EXPECT_TBODY:
                if re.search("<tbody", l):
                    parse_state = EXPECT_MUTANT_TYPE
            elif parse_state == EXPECT_MUTANT_TYPE:
                m = re.search("<td.*?>(.+?)<sub>(\d+?)</sub>", l)
                if m:
                    mutant, num = m.groups()
                    current_program['equivalent_mutants'].append({
                        'mutant': mutant,
                        'num': num
                    })

    #finalize last program
    if current_program:
        programs.append(current_program)

    return programs

def filter_ndiff(diff):
    #print ''.join( difflib.ndiff(l, r))
    def filter(i):
        if i[0] == ' ':
            return False
        elif i[0] == '+':
            return True
        elif i[0] == '-':
            return True
        elif i[0] == '?':
            return True
        sys.stdout.write(i)
    for i in diff:
        if filter(i):
            yield i

def tag_equivalent_variants(programs, args):
    # to aid our review process, we want to present a VIM window with:
    # 1. the original source
    # 2. the equivalent source
    # 3. a (comma,newline) seperated file full of tags to apply to each mutant
    # we review?? if there are already tags, we show that file?
    
    path_map = { 
        "Bisect": "result/Bisect/traditional_mutants/double_sqrt(double)/"
        , "Commons-Lang: capitalize" : "result/org.apache.commons.lang.WordUtils/traditional_mutants/java.lang.String_capitalize(java.lang.String,char)/"
        , "Commons-Lang: wrap": "result/org.apache.commons.lang.WordUtils/traditional_mutants/java.lang.String_wrap(java.lang.String,int,java.lang.String,boolean)/"
        , "Joda-Time: add": "result/org.joda.time.chrono.BasicMonthOfYearDateTimeField/traditional_mutants/long_add(long,int)/"
        , "Pamvotis: addNode": "result/pamvotis.core.Simulator/traditional_mutants/void_addNode(int,int,int,int,int,int)/"
        , "Pamvotis: removeNode": "result/pamvotis.core.Simulator/traditional_mutants/boolean_removeNode(int)/"
        , "Triangle": "result/tr.Triangle/traditional_mutants/int_classify(int,int,int)/"
        , "XStream": "result/xcom.thoughtworks.xstream.io.xml.XmlFriendlyNameCoder/traditional_mutants/java.lang.String_decodeName(java.lang.String)/"
    }
    source_map = {
        "Bisect": "Bisect.java"
        , "Commons-Lang: capitalize" : "WordUtils.java"
        , "Commons-Lang: wrap": "WordUtils.java"
        , "Joda-Time: add": "BasicMonthOfYearDateTimeField.java"
        , "Pamvotis: addNode": "Simulator.java"
        , "Pamvotis: removeNode": "Simulator.java"
        , "Triangle": "Triangle.java"
        , "XStream": "XmlFriendlyNameCoder.java"
    }
    original_map = {name:os.path.join(path_map[name],'../../original',f) for name,f in source_map.iteritems()}
    #original_map = {
        #"Bisect": "result/Bisect/original/Bisect.java"
        #, "Commons-Lang: capitalize" : "result/org.apache.commons.lang.WordUtils/original/WordUtils.java"
        #, "Commons-Lang: wrap": "result/org.apache.commons.lang.WordUtils/original/WordUtils.java"
        #, "Joda-Time: add": "result/org.joda.time.chrono.BasicMonthOfYearDateTimeField/original/BasicMonthOfYearDateTimeField.java"
        #, "Pamvotis: addNode": "result/pamvotis.core.Simulator/original/Simulator.java"
        #, "Pamvotis: removeNode": "result/pamvotis.core.Simulator/original/Simulator.java"
        #, "Triangle": "result/tr.Triangle/original/Triangle.java"
        #, "XStream": "result/xcom.thoughtworks.xstream.io.xml.XmlFriendlyNameCoder/original/XmlFriendlyNameCoder.java"
    #}
    
    for p in programs:
        benchmark = p['benchmark']
        mutants = p['equivalent_mutants']

        if benchmark not in path_map:
            raise ValueError("{} not in path_map, so can't find mutants location!".format(p['benchmark']))
        path = path_map[benchmark]
        if not os.path.exists(path):
            raise ValueError("{} does not exist! Read README.md and run make to generate mutants.".format(path))

        if benchmark not in original_map:
            raise ValueError("{} not in original_map, so can't find original location!".format(p['benchmark']))
        #original = original_map[benchmark]
        original = original_map[benchmark]
        if not os.path.exists(original):
            raise ValueError("{} does not exist! Read README.md and run make to generate mutants.".format(original))

        #for the diff, read the original into an array of lines
        def readlines(f):
            with open(f, "r") as fh:
                return [line for line in fh]

        original_lines = readlines(original)

        for m in mutants:
            variant_name = "{}_{}".format(m['mutant'], m['num'])
            mutant_path = os.path.join( path, variant_name, source_map[benchmark])
            #verify mutant exists
            if not os.path.exists(mutant_path):
                raise ValueError("{} mutant does not exist! Read README.md and run make to generate mutants.".format(mutant_path))

            # compute a diff that we store as part of the json to make it easy
            # to examine variants after tagging
            print "tags: {}".format(m)
            mutant_lines = readlines(mutant_path)
            diff = filter_ndiff(difflib.ndiff(original_lines, mutant_lines))
            compact_diff = ''.join(diff)
            m['diff'] = compact_diff

            if args.skip_tagged and len(m.get('tags', [])) > 0:
                print "skipping {} because already tagged".format(mutant_path)
                continue


            if args.filter_tags:
                match = False
                matched_filer = None
                for f in args.filter_tags:
                    for t in m.get('tags', []):
                        if re.search(f, t):
                            matched_filter = f
                            match = True
                            break
                    if match:
                        break
                if match:
                    print "skipping {} because filter {} matched".format(mutant_path, matched_filter)
                    continue

            print "editing {}".format(mutant_path)

            #figure out the right spot to put tags
            #IMO we should output a json file so the resulsts are easy to read
            # so we'll write to a tmp file, and read it back into the json as
            # an array
            tmp_file = tempfile.NamedTemporaryFile(mode="w+", delete=True)
            tags_file = tmp_file.name
            if 'tags' in m:
                tmp_file.write(", ".join(m['tags']))
                tmp_file.flush()

            #loop in case we make mistakes
            cont = 'r' #repeat by default unless we go next or no
            while cont != 'y':
                # btw vim works only when we aren't redirecting stdin
                cmd_args = ['vim','-d'
                    , original, mutant_path
                    , "+:top split | view manual_analysis_questions.txt"
                    , "+:resize 10"
                    , "+:bot split +:edit {tags}".format(tags=tags_file)
                    , "+:resize 2"
                ]
                subprocess.call(cmd_args)
                #subprocess.call(['reset'])

                tmp_file.seek(0)
                tags = tmp_file.read()
                tags = [s.strip() for s in tags.split(',')]
                m['tags'] = tags
                print "parsed tags for variant {}: {}".format(variant_name, tags)

                cont = raw_input('continue? (y|n|r)')
                if cont == 'n':
                    return
                    #sys.exit(1)

            #shell_cmd = re.sub("[\(\)]", "\\\1", " ".join(args))
            #print shell_cmd
            #os.system(shell_cmd)
            save_programs(programs, args)

            pass

def save_programs(programs, args):
    if args.output:
        with open(args.output, "w+") as out:
            json.dump(programs, out, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='read the html page on the manually verified mutants from TCE and tag each one with relevant codes')
    parser.add_argument('--file', '-f', required=True, help="the html page from TCE")
    parser.add_argument('--output', '-o', required=True, help="the output json file")
    parser.add_argument('--skip_tagged', '-s', action="store_true")
    parser.add_argument('--filter_tags', '-t', action='append', help="filter out programs when tags match the expression")
    args = parser.parse_args()

    programs = None

    # if the output file already exists, use it as the program instead
    if args.output and os.path.exists(args.output):
        print "loading existing program json"
        try:
            with open(args.output) as fh:
                programs = json.load(fh)
        except ValueError as e:
            print "error parsing json"
            print e
            programs = None

    if not programs:
        print "parsing html file to create new program json"
        with open(args.file) as fh:
            programs = parse_programs(fh)

    tag_equivalent_variants(programs, args)

    save_programs(programs, args)
