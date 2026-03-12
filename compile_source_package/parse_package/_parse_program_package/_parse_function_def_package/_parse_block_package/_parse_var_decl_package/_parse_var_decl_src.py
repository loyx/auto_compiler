# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Lazy import to avoid circular dependency issues
def _get_parse_expression():
    from ._parse_expression_package._parse_expression_src import _parse_expression
    return _parse_expression

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_var_decl(parser_state: dict) -> dict:
    """解析变量声明。输入：当前位置指向类型标识符 token。输出：VAR_DECL AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected type identifier")
    
    # 解析类型标识符
    type_token = tokens[pos]
    valid_types = {
        "INT": "int",
        "FLOAT": "float",
        "BOOL": "bool",
        "STRING": "string"
    }
    
    if type_token["type"] == "IDENTIFIER":
        var_type = type_token["value"]
    elif type_token["type"] in valid_types:
        if type_token["value"] != valid_types[type_token["type"]]:
            raise SyntaxError(f"Expected type identifier, got {type_token['type']}")
        var_type = type_token["value"]
    else:
        raise SyntaxError(f"Expected type identifier, got {type_token['type']}")
    
    line = type_token["line"]
    column = type_token["column"]
    pos += 1
    
    # 消费变量名
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected variable name")
    
    name_token = tokens[pos]
    if name_token["type"] != "IDENTIFIER":
        raise SyntaxError(f"Expected variable name, got {name_token['type']}")
    
    var_name = name_token["value"]
    pos += 1
    
    # 构建 VAR_DECL 节点
    var_decl_node = {
        "type": "VAR_DECL",
        "children": [],
        "value": {
            "var_type": var_type,
            "var_name": var_name
        },
        "line": line,
        "column": column
    }
    
    # 可选：解析初始化表达式
    if pos < len(tokens) and tokens[pos]["type"] == "ASSIGN":
        pos += 1  # 消费等号
        parse_expr = _get_parse_expression()
        init_expr = parse_expr(parser_state)
        parser_state["pos"] = pos  # 更新位置
        var_decl_node["children"].append(init_expr)
    else:
        parser_state["pos"] = pos
    
    # 可选：消费分号
    if pos < len(tokens) and tokens[pos]["type"] == "SEMICOLON":
        parser_state["pos"] = pos + 1
    
    return var_decl_node

# === helper functions ===

# === OOP compatibility layer ===
