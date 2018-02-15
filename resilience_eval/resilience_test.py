#!/usr/bin/env python
import json
import argparse
import os
from pprint import pprint
import subprocess
import sys
import hashlib
import re

#templates used to generate code
import resilience_templates

def util_hash(hash_object, file_path):
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_object.update(chunk)
    return hash_object.hexdigest()

def util_sha256_hash(file_path):
    return util_hash(hashlib.sha256(), file_path)

def generate_scala_code(program, args):
    pass

# return hash or false if error
def gcc_compile_and_hash(program, variant_idx, variant_path, program_text):
    #OS X gcc is ACTUALLY CLANG so we use one from homebrew
    # TODO use a much more recent version of gcc
    asm_path = "{}.S".format(variant_path)
    compile_cmd = "/usr/local/bin/gcc-4.9 -o {} -c -S -O3 -std=gnu11 {}.c".format(asm_path, variant_path)
    #compile_cmd = "clang -o {} -c -S -O3 {}.c".format(asm_path, variant_path)
    print compile_cmd

    try:
        output = subprocess.check_output(compile_cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as cpe:
        print "{} returned {}".format(compile_cmd, cpe.returncode)
        print cpe.output
        return False

    # program is compiled, so hash asm
    h = util_sha256_hash(asm_path)

    return h

def generate_c_code(program, args):
    #program_dir = os.path.join(args.output_dir, 'c', program['name'])

    type_map = resilience_templates.CProgram.type_map

    #generate type signature for input, passing it through the type map to get C types
    input_types = [ type_map.get(ty,ty)  for ty in program.get('input_types', []) ]
    input_sig = [ '{t} input{i}'.format(t=ty, i=idx) for idx,ty in enumerate(input_types) ]
    inputs = ', '.join( input_sig )

    # !!! watch out for the mutability and potential cycles 
    return_type = type_map.get(program['return_type'], program['return_type'])

    # if there isn't a default return insert one
    return_stmnt = program.get('return', 'return')

    body = resilience_templates.CProgram.body
    program_hashes = []
    for idx,v in enumerate(program.get('variants', [])):
        if 'code' not in v:
            print 'skipping variant {} for {} because no compatible code specified'.format(
                idx, program['name']
            )
            continue
        program_text = body.format(
            expression=v['code']
            , return_type = return_type
            , name = program['name']
            , inputs = inputs
            , return_stmnt=return_stmnt
        )

        # computed variant path lacks extension, be mindful of this.
        variant_path = os.path.join(args.output_dir, 'c', '{}-{}'.format(program['name'], idx) )
        code_path = "{}.c".format(variant_path)

        # we chose to write to files because this is easier to debug mismatches
        if not os.path.exists(os.path.dirname(code_path)):
            os.makedirs(os.path.dirname(code_path))
        with open(code_path, "w+") as fh:
            fh.write(program_text)

        if True: #if debug:
            print "****** {}".format(code_path)
            pprint(program, indent=4)
            print program_text

        #todo general compiler interface
        ret = gcc_compile_and_hash(program, idx, variant_path, program_text)
        if not ret:
            # test failure
            sys.exit(1)
        else:
            print "success"
            program_hashes.append(ret)

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
        #generate_scala_code(p, args)
        program_hashes = generate_c_code(p, args)

        # i think it would be good to save a report, so we add a variant_hashes
        # member to the program dict and output it
        unique_hashes = list(set(program_hashes)) # cast set back to list for json serializability
        p['tested_on'] = 'GCC 4.9 O3'
        p['program_hashes'] = program_hashes
        p['unique_hashes'] = unique_hashes
        p['success_overall'] = len(unique_hashes) == 1
        p['success_partial'] = len(unique_hashes) < len(p['variants'])
        p['failure_total'] = len(unique_hashes) == len(p['variants'])
        total_unique_programs = total_unique_programs + len(unique_hashes)
        total_variants = total_variants + len(program_hashes)

    overall['total_programs'] = len(overall.get('programs', []))
    overall['total_unique_programs'] = total_unique_programs
    overall['total_variants'] = total_variants

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
    args = parser.parse_args()

    with open(args.filename) as fh:
        program = json.load(fh)

    clean_programs(program)

    generate_all_code(program, args)

    if(args.report_output):
         with open(args.report_output, 'w+') as fh:
             json.dump(program, fh, indent=4)

    #pprint(program, indent=4)

if __name__ == "__main__":
    main()
