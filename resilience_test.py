#!/usr/bin/env python
import json
import argparse
import os
from pprint import pprint

#templates used to generate code
import resilience_templates

def generate_scala_code(program, args):
    pass

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
    ret = program.get('return', 'return')

    for idx,v in enumerate(program.get('variants', [])):
        variant_path = os.path.join(args.output_dir, 'c', '{}-{}.c'.format(program['name'], idx) )

        body = resilience_templates.CProgram.body
        print "****** {}".format(variant_path)
        pprint(program, indent=4)
        print body.format(
            expression=v['code']
            , return_type = return_type
            , name = program['name']
            , inputs = inputs
            , return_stmnt=ret
        )
        pass

def generate_all_code(overall, args):
    # generate scala and c code from the programs
    # do the general purpose input substitution
    #
    # TODO the larger code examples might not fit into this framework
    # but i'm trying this anyways?
    for p in overall.get('programs', []):
        generate_scala_code(p, args)
        generate_c_code(p, args)

    pass

def main():
    parser = argparse.ArgumentParser(description='run resilience test using input')
    parser.add_argument('--filename', '-f', help='filename of resilience test definitions', required=True)
    parser.add_argument('--output_dir', '-o', help='output directory for code generation', required=True)
    args = parser.parse_args()

    with open(args.filename) as fh:
        program = json.load(fh)

    generate_all_code(program, args)

if __name__ == "__main__":
    main()
