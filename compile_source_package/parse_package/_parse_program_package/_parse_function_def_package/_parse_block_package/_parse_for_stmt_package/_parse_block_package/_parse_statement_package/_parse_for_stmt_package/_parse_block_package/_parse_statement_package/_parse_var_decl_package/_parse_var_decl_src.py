# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_var_decl(parser_state: ParserState) -> AST:
    """
    解析变量声明语句：var/let name [: Type] [= value];
    返回 VAR_DECL AST 节点，原地更新 parser_state["pos"]。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]

    # 步骤 1: 消耗 VAR 或 LET token
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 意外的文件结束，期望变量声明")
    
    keyword_token = tokens[pos]
    if keyword_token["type"] not in ("VAR", "LET"):
        raise SyntaxError(
            f"{filename}:{keyword_token['line']}:{keyword_token['column']}: "
            f"期望 VAR 或 LET，得到 {keyword_token['type']}"
        )
    start_line = keyword_token["line"]
    start_column = keyword_token["column"]
    pos += 1

    # 步骤 2: 期望 IDENT token 作为变量名
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{start_line}:{start_column}: 意外的文件结束，期望变量名")
    
    name_token = tokens[pos]
    if name_token["type"] != "IDENT":
        raise SyntaxError(
            f"{filename}:{name_token['line']}:{name_token['column']}: "
            f"期望变量名 (IDENT)，得到 {name_token['type']}"
        )
    var_name = name_token["value"]
    pos += 1

    # 步骤 3: 检查类型注解 (可选)
    type_annotation = None
    if pos < len(tokens) and tokens[pos]["type"] == "COLON":
        pos += 1  # 消耗 COLON
        if pos >= len(tokens):
            raise SyntaxError(f"{filename}:{start_line}:{start_column}: 意外的文件结束，期望类型注解")
        
        type_token = tokens[pos]
        if type_token["type"] != "IDENT":
            raise SyntaxError(
                f"{filename}:{type_token['line']}:{type_token['column']}: "
                f"期望类型名 (IDENT)，得到 {type_token['type']}"
            )
        type_annotation = type_token["value"]
        pos += 1

    # 步骤 4: 检查初始化值 (可选)
    value_ast = None
    if pos < len(tokens) and tokens[pos]["type"] == "EQUAL":
        pos += 1  # 消耗 EQUAL
        # 此时 pos 指向表达式第一个 token，调用 _parse_expression
        value_ast = _parse_expression(parser_state)
        pos = parser_state["pos"]  # 更新 pos 到表达式结束位置

    # 步骤 5: 消耗 SEMICOLON (如果存在)
    if pos < len(tokens) and tokens[pos]["type"] == "SEMICOLON":
        pos += 1

    # 更新 parser_state 位置
    parser_state["pos"] = pos

    # 返回 VAR_DECL AST 节点
    return {
        "type": "VAR_DECL",
        "name": var_name,
        "value": value_ast,
        "type_annotation": type_annotation,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node