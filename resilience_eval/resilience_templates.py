
class CProgram:
    type_map = {
            "boolean": "int" #map boolean to int for now
    }
    body = """
{header}
{return_type} {name}({inputs}){{
    {return_stmnt} {expression};
}}
"""

class JavaProgram:
    type_map = {
            "boolean": "boolean" #map boolean to int for now
            , "int*": "int[]"
            , "char*": "char[]"
            , "int**": "int[][]"
    }
    body = """
{header}
class {name} {{
    {class_header}
    {return_type} {name}({inputs}){{
        {return_stmnt} {expression}
    }}
}}
"""

class ScalaProgram:
    type_map = {
            "boolean": "Boolean" #map boolean to int for now
            , 'int': 'Int'
            , 'long': 'Long'
            , 'char': 'Char'
            , "int*": "Array[Int]"
            , "char*": "Array[Char]"
            , "int**": "Array[Array[Int]]"
            , 'void': 'Unit'
    }
    body = """
{header}
object {name} {{
    {class_header}
    def {name}({inputs}): {return_type} = {{
        {return_stmnt} {expression}
    }}
}}
"""
