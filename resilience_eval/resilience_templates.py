
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
