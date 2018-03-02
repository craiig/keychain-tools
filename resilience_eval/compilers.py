# abstract compiler class
# goal here is to provide a number of different compilers that implement the
# same set of functionality so we can try our benchmarks on multiple different
# compilers at once
import os, shutil
from pprint import pprint
import subprocess

from util import util_sha256_hash
import resilience_templates

class Compiler(object):

    def __init__(self):
        pass

    def name(self):
        raise ValueError("no name function defined")

    def supported_languages(self):
        print "warning: implement your supported languages function"

    # generate_code and compile_and_hash are split so that we can enforce code
    # is generated and placed in the right build folder to support debugging
    # this is basically the only reason 

    # return a file path or false
    def generate_code(self, variant, program, output_dir):
        print "warning: implement your code generation function"

    # return a hash or false
    def compile_and_hash(self, variant_path, program):
        print "warning: implement your compile and hash function"

class CCompiler(Compiler):

    def __init__(self, compiler_name, opt_level):
        compiler_map = {
                #TODO verify versions are correct in the calls here
                "gcc49": "/usr/local/bin/gcc-4.9 -o {asm_path} -c -S {opt_level} -std=gnu11 {variant_path}.c"
                , "clang": "clang -o {asm_path} -c -S {opt_level} {variant_path}.c"
        }
        self.compiler_name = compiler_name
        self.compiler_template = compiler_map[compiler_name]
        self.opt_level = opt_level

    def name(self):
        return "{name}_{opt_level}".format(name=self.compiler_name,
                opt_level=self.opt_level)

    def supported_languages(self):
        return ["c"]

    def c_codegen(self, variant, program, output_dir):
        type_map = resilience_templates.CProgram.type_map

        #generate type signature for input, passing it through the type map to get C types
        input_types = [ type_map.get(ty,ty)  for ty in program.get('input_types', []) ]
        input_sig = [ '{t} input{i}'.format(t=ty, i=tyidx) for tyidx,ty in enumerate(input_types) ]
        inputs = ', '.join( input_sig )

        # !!! watch out for the mutability and potential cycles 
        return_type = type_map.get(program['return_type'], program['return_type'])

        # if there isn't a default return insert one
        return_stmnt = program.get('return', 'return')

        header_stmnt = program.get('header', '')

        body = resilience_templates.CProgram.body

        # TODO hoist all above code into a class?
        program_text = body.format(
            expression=variant['code']
            , return_type = return_type
            , name = program['name']
            , inputs = inputs
            , return_stmnt=return_stmnt
            , header=header_stmnt
        )

        # computed variant path lacks extension, be mindful of this.
        idx = variant['_idx']
        variant_path = os.path.join(output_dir, 'c', self.name(), '{}-{}'.format(program['name'], idx) )
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

        return variant_path

    #returns a file path with the generated variant
    def generate_code(self, variant, program, output_dir):
        if 'code' in variant:
            return self.c_codegen(variant, program, output_dir)
        elif 'type' in variant:
            if variant['type'] == 'file':
                #copy to output dir so it's easy to handle
                variant_path = os.path.join(output_dir, 'c', self.name(),  '{}-{}'.format(program['name'], variant['_idx']) )
                code_path = "{}.c".format(variant_path)
                if 'c' in variant:
                    shutil.copyfile(variant['c'], code_path)
                return variant_path

    # accept path to a file and the program spec. the program spec is used to find
    # the relevant function to be hashed. this can help when testing function
    # inlining behaviours and there are addition functions in the output bytecode.
    # returns hash or false if error
    def compile_and_hash(self, variant_path, program):
        #OS X gcc is ACTUALLY CLANG so we use one from homebrew
        # TODO use a much more recent version of gcc
        asm_path = "{}.S".format(variant_path)
        #compile_cmd = "/usr/local/bin/gcc-4.9 -o {} -c -S -O3 -std=gnu11 {}.c".format(asm_path, variant_path)
        #compile_cmd = "clang -o {} -c -S -O3 {}.c".format(asm_path, variant_path)
        compile_cmd = self.compiler_template.format(
            asm_path = asm_path,
            variant_path = variant_path,
            opt_level = self.opt_level
        )
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

CompilerDefinitions = [
    #JavaCompiler(),
    #ScalaCompiler(),
    CCompiler('gcc49', '-O0'),
    CCompiler('gcc49', '-O3'),
    CCompiler('clang', '-O0'),
    CCompiler('clang', '-O3')
]
