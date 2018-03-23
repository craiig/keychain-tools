
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
    }
    body = """
{header}
class {name} {{
    {return_type} {name}({inputs}){{
        {return_stmnt} {expression}
    }}
}}
"""
