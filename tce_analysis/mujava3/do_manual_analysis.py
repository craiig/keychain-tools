#!/usr/bin/python
# basic script to parse the manually verified equivalent mutants and extract
# them from the generated mutants

import sys
import re
import json
import subprocess
import os
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

def tag_equivalent_variants(programs):
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
        pprint(p)
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

        for m in mutants:
            mutant_path = os.path.join( path, "{}_{}".format(m['mutant'], m['num']), source_map[benchmark])
            #verify mutant exists
            if not os.path.exists(mutant_path):
                raise ValueError("{} mutant does not exist! Read README.md and run make to generate mutants.".format(mutant_path))

            #vim doesn't quite work, so instead let's use the built in diff tools we use for the HLS trace analysis
            #args = ['vim','-d', original, mutant_path]
            #subprocess.call(args)
            #subprocess.call(['reset'])

            cont = raw_input('continue? (y|n)')
            if cont != 'y':
                sys.exit(1)

            print 'supposed to continue'
            sys.exit(1)

            #shell_cmd = re.sub("[\(\)]", "\\\1", " ".join(args))
            #print shell_cmd
            #os.system(shell_cmd)
            
            print mutant_path
            pass

if __name__ == "__main__":
    programs = parse_programs(sys.stdin)
    tag_equivalent_variants(programs)
