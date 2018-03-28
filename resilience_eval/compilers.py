# abstract compiler class
# goal here is to provide a number of different compilers that implement the
# same set of functionality so we can try our benchmarks on multiple different
# compilers at once
import os, shutil
from pprint import pprint
import subprocess

from util import util_sha256_hash
import resilience_templates

def subprocess_exception_catch(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as cpe:
        print "{} returned {}".format(cmd, cpe.returncode)
        print cpe.output
        return False
    return True

class Compiler(object):

    def __init__(self):
        pass

    def name(self):
        raise ValueError("no name function defined")

    def supported_languages(self):
        raise ValueError("implement your supported languages function")

    # generate_code and compile_and_hash are split so that we can enforce code
    # is generated and placed in the right build folder to support debugging
    # this is basically the only reason 

    # return a file path or false
    def generate_code(self, variant, program, code_path):
        raise ValueError("implement the code generation function")

    # return a hash or false
    def compile_and_hash(self, variant_path, program):
        raise ValueError("implement the compile and hash function")


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

    def c_codegen(self, variant, program, code_path):
        type_map = resilience_templates.CProgram.type_map

        #generate type signature for input, passing it through the type map to get C types
        input_types = [ type_map.get(ty,ty)  for ty in program.get('input_types', []) ]
        input_sig = [ '{t} input{i}'.format(t=ty, i=tyidx) for tyidx,ty in enumerate(input_types) ]
        inputs = ', '.join( input_sig )

        # !!! watch out for the mutability and potential cycles 
        return_type = type_map.get(program['return_type'], program['return_type'])

        # if there isn't a default return insert one
        return_stmnt = program.get('return', 'return')

        # append c_header to header
        header_stmnt = program.get('header', '')
        header_stmnt += program.get('c_header', '')

        body = resilience_templates.CProgram.body

        if 'c_code' in variant:
            expression = variant['c_code']
        else:
            expression = variant['code']

        # TODO hoist all above code into a class?
        program_text = body.format(
            expression=expression
            , return_type = return_type
            , name = program['name']
            , inputs = inputs
            , return_stmnt=return_stmnt
            , header=header_stmnt
        )

        # we chose to write to files because this is easier to debug mismatches
        if not os.path.exists(os.path.dirname(code_path)):
            os.makedirs(os.path.dirname(code_path))
        with open(code_path, "w+") as fh:
            fh.write(program_text)

        if True: #if debug:
            print "****** {}".format(code_path)
            pprint(program, indent=4)
            print program_text

        return True

    #returns a file path with the generated variant
    def generate_code(self, variant, program, code_path):
        return self.c_codegen(variant, program, code_path)

    # accept path to a file and the program spec. the program spec is used to find
    # the relevant function to be hashed. this can help when testing function
    # inlining behaviours and there are addition functions in the output bytecode.
    # returns hash or false if error
    def compile_and_hash(self, variant_path, program):
        #OS X gcc is ACTUALLY CLANG so we use one from homebrew
        # TODO use a much more recent version of gcc
        asm_path = "{}.S".format(variant_path)
        if not os.path.exists(asm_path):
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
        else:
            print 'skipping compile because asm path exists: {}'.format(asm_path)

        # program is compiled, so hash asm
        h = util_sha256_hash(asm_path)

        return h

class JavaCompiler(Compiler):
    def __init__(self, path):
        self.compiler_template = "{path} {variant_path}.java"

        self.path = path
        self.version = subprocess.check_output("{} -version".format(path), shell=True, stderr=subprocess.STDOUT)
        self.version = self.version.strip(' \n\t')
        self.version = self.version.replace(' ', '')
        pass

    def name(self):
        return self.version

    def supported_languages(self):
        return ["java"]

    def java_codegen(self, variant, program, code_path):
        type_map = resilience_templates.JavaProgram.type_map

        #generate type signature for input, passing it through the type map to get C types
        input_types = [ type_map.get(ty,ty)  for ty in program.get('input_types', []) ]
        input_sig = [ '{t} input{i}'.format(t=ty, i=tyidx) for tyidx,ty in enumerate(input_types) ]
        inputs = ', '.join( input_sig )

        # !!! watch out for the mutability and potential cycles 
        return_type = type_map.get(program['return_type'], program['return_type'])

        if 'java_code' in variant:
            expression = variant['java_code']
        else:
            expression = variant['code']

        # if there isn't a default return insert one
        return_stmnt = program.get('return', 'return')
        if len(return_stmnt) > 0:
            #could propagate to the c compiler too
            #but it's less strict
            expression += ';'

        header_stmnt = program.get('header', '')
        header_stmnt += program.get('java_header', '')

        body = resilience_templates.JavaProgram.body

        # TODO hoist all above code into a class?
        program_text = body.format(
            expression=expression
            , return_type = return_type
            , name = program['name']
            , inputs = inputs
            , return_stmnt=return_stmnt
            , header=header_stmnt
            , class_header = program.get('java_class_header',  '')
        )

        # we chose to write to files because this is easier to debug mismatches
        if not os.path.exists(os.path.dirname(code_path)):
            os.makedirs(os.path.dirname(code_path))
        with open(code_path, "w+") as fh:
            fh.write(program_text)

        if True: #if debug:
            print "****** {}".format(code_path)
            pprint(program, indent=4)
            print program_text

        return True

    def generate_code(self, variant, program, code_path):
        return self.java_codegen(variant, program, code_path)

    # TODO i think we need to write a CLI library for the udf-hashing
    # program so we can use it to disassemble compiled java?
    # otheriwse we can use javap -c ...
    # 
    # gonna try javap -c for now, could be an option in the future
    def compile_and_hash(self, variant_path, program):
        # challenge here is javac produces an object file that corresponds
        # to the class name. how to catch it?
        # generate with specific class name (proram name)
        asm_path = variant_path + '.bc'
        if not os.path.exists(asm_path):
            compile_cmd = self.compiler_template.format(
                path = self.path,
                variant_path = variant_path,
            )
            print compile_cmd
            res = subprocess_exception_catch(compile_cmd)
            if not res:
                return False

            # read the bytecode off the class
            class_file = os.path.join(os.path.dirname(variant_path), program['name']) + '.class'
            bytecode_cmd = "javap -c {} > {}".format(class_file, asm_path)
            res = subprocess_exception_catch(bytecode_cmd)
            if not res:
                return False

        # program is compiled, so hash asm
        h = util_sha256_hash(asm_path)
        return h

CompilerDefinitions = [
    JavaCompiler("javac"),
    #ScalaCompiler(),
    CCompiler('gcc49', '-O0'),
    CCompiler('gcc49', '-O3'),
    CCompiler('clang', '-O0'),
    CCompiler('clang', '-O3')
]