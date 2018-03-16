#!/usr/bin/env python
import json
import argparse
import os, shutil
from pprint import pprint
import sys
import re

#templates used to generate code
import resilience_templates
from compilers import CompilerDefinitions

def generate_scala_code(program, args):
    pass

def perform_tests(program, args):
    program_hashes = {}
    for idx,v in enumerate(program.get('variants', [])):
        for compiler in CompilerDefinitions:
            print compiler.name()
            v['_idx'] = idx

            variant_path = compiler.generate_code(v, program, args.output_dir)
            print "variant path: {}".format(variant_path)

            if not variant_path:
                print 'skipping variant {} for {} because no compatible code specified'.format(
                    idx, program['name']
                )
                #raise ValueError("please make all programs work on all compilers")
                continue

            #todo general compiler interface
            ret = compiler.compile_and_hash(variant_path, program)
            if not ret:
                # test failure
                print "test failure"
                sys.exit(1)
            else:
                print "success"
                compiler_name = compiler.name()
                if compiler_name not in program_hashes:
                    program_hashes[compiler_name] = []
                program_hashes[compiler_name].append(ret)

    # after variant loop hash
    return program_hashes

def generate_all_code(overall, args):
    # generate scala and c code from the programs
    # do the general purpose input substitution
    #
    # TODO the larger code examples might not fit into this framework
    # but i'm trying this anyways?
    total_variants = 1
    total_unique_programs = 0
    for p in overall.get('programs', []):
        # uncomment to only do a specific eval
        #if p['name'] != 'constant_folding_associativity':
            #continue
        
        visit = (args.filter_programs == None)
        if not visit: #i.e. filter programs is not none
            for ft in args.filter_programs:
                m = re.match(ft, p['name'])
                if m:
                    print "{} re.match {}, visiting".format(ft, p['name'])
                    visit = True
                    break
        if not visit:
            print "skipping {} due to no filter match".format(p['name'])
            continue

        program_hashes = perform_tests(p, args)
        p['program_hashes'] = program_hashes

        # i think it would be good to save a report, so we add a variant_hashes
        # member to the program dict and output it
        # old stats from before the addition of multi-compilers
        #unique_hashes = list(set(program_hashes)) # cast set back to list for json serializability
        #p['unique_hashes'] = unique_hashes
        #p['success_overall'] = len(unique_hashes) == 1
        #p['success_partial'] = len(unique_hashes) < len(p['variants'])
        #p['failure_total'] = len(unique_hashes) == len(p['variants'])
        #total_unique_programs = total_unique_programs + len(unique_hashes)
        #total_variants = total_variants + len(program_hashes)

    # old stats from before the addition of multi-compilers
    #overall['total_unique_programs'] = total_unique_programs
    #overall['total_variants'] = total_variants

def analyze_programs_minmax(overall):
    #one way to look at these stats is to do min/max:
    # what is the minimum number of unique hashes? one per program
    # maximum? one per variant

    total_variants = 0
    compiler_results = {}
    per_origin = {}
    for p in overall['programs']:
        total_variants = total_variants + len(p['variants'])

        origin = p['origin'] #get program origin to classify
        per_origin[origin] = per_origin.get(origin, {}) #create if not exists
        origin_stats = per_origin[origin] # look up
        origin_stats['total_programs'] = origin_stats.get('total_programs', 0) + 1
        origin_stats['total_variants'] = origin_stats.get('total_variants', 0) + len(p['variants'])

        #iterate over each compiler's results
        for c in p['program_hashes'].iterkeys():
            program_hashes = p['program_hashes'][c]
            unique_hashes = list(set(program_hashes)) # cast set back to list for json serializability

            if c not in compiler_results:
                compiler_results[c] = {'origins':{}}
            cr = compiler_results[c]

            cr['unique_hashes'] = cr.get('unique_hashes', 0) + len(unique_hashes)

            # break these out by benchmark so we can get an idea of each one does
            if origin not in cr['origins']:
                cr['origins'][origin] = {}
            cro = cr['origins'][origin]
            cro['unique_hashes'] = cro.get('unique_hashes', 0) + len(unique_hashes)

    overall['total_programs'] = len(overall.get('programs', []))
    overall['total_compiler_results'] = compiler_results
    overall['total_variants'] = total_variants
    overall['total_origin_stats'] = per_origin

def analyze_program_tests_success(overall):
    # analyze success from the perspective of whether or not a particular test passed or failed
    # pass = a single hash
    
    compilers_pass_fail = {}

    for p in overall['programs']:
        origin = p['origin'] #get program origin to classify
        for c in p['program_hashes'].iterkeys():
            if c not in compilers_pass_fail:
                compilers_pass_fail[c] = {'passes': 0, 'fails': 0, 'passed_tests': [], 'failed_tests': [], 'origins':{}}
            cr = compilers_pass_fail[c]

            if origin not in cr['origins']:
                cr['origins'][origin] = {'passes': 0, 'fails': 0, 'passed_tests': [], 'failed_tests': []}

            program_hashes = p['program_hashes'][c]
            unique_hashes = list(set(program_hashes)) # cast set back to list for json serializability
            if len(unique_hashes) > 1:
                cr['fails'] += 1
                cr['origins'][origin]['fails'] += 1
                cr['origins'][origin]['failed_tests'].append(p['name'])
            else:
                cr['passes'] += 1
                cr['origins'][origin]['passes'] += 1
                cr['origins'][origin]['passed_tests'].append(p['name'])

    overall['total_compiler_pass_fail'] = compilers_pass_fail

def clean_programs(program):
    for p in program['programs']:
        if re.search(' ', p['name']):
            newname = re.sub(r' ', '_', p['name'])
            print >> sys.stderr, "warning: renaming '{}' to {}".format(p['name'], newname)
            p['name'] = newname

def main():
    parser = argparse.ArgumentParser(description='run resilience test using input')
    parser.add_argument('--filename', '-f', help='filename of resilience test definitions', required=True)
    parser.add_argument('--output_dir', '-o', help='output directory for code generation', required=True)
    parser.add_argument('--report_output', '-r', help='output destination for report')
    parser.add_argument('--filter_programs', '-fp', help='only run selected programs', action='append')
    args = parser.parse_args()

    with open(args.filename) as fh:
        program = json.load(fh)

    clean_programs(program)

    generate_all_code(program, args)

    analyze_programs_minmax(program)
    analyze_program_tests_success(program)

    if(args.report_output):
         with open(args.report_output, 'w+') as fh:
             json.dump(program, fh, indent=4)

    #pprint(program, indent=4)

if __name__ == "__main__":
    main()
