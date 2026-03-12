# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

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
#   "type": str,             # 节点类型 (PROGRAM, FUNCTION_DEF, PARAM, VAR_DECL, IF_STMT, WHILE_STMT, FOR_STMT, RETURN_STMT, BREAK_STMT, CONTINUE_STMT, EXPR_STMT, BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, BLOCK)
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
def _parse_var_decl(parser_state: ParserState) -> AST:
    """
    解析变量声明语句。
    语法格式：let identifier = expression; 或 var identifier = expression;
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 步骤 1: 消耗 LET/VAR token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected 'let' or 'var'")
    
    keyword_token = tokens[pos]
    if keyword_token["type"] not in ("LET", "VAR"):
        raise SyntaxError(f"Expected 'let' or 'var', got '{keyword_token['value']}'")
    
    keyword = keyword_token["value"]
    line = keyword_token["line"]
    column = keyword_token["column"]
    pos += 1
    
    # 步骤 2: 解析标识符（变量名）
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected identifier")
    
    ident_token = tokens[pos]
    if ident_token["type"] != "IDENTIFIER":
        raise SyntaxError(f"Expected identifier, got '{ident_token['value']}'")
    
    var_name = ident_token["value"]
    pos += 1
    
    # 步骤 3: 消耗等号 token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected '='")
    
    equals_token = tokens[pos]
    if equals_token["type"] != "EQUALS":
        raise SyntaxError(f"Expected '=', got '{equals_token['value']}'")
    
    pos += 1
    
    # 步骤 4: 解析初始化表达式
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected expression")
    
    parser_state["pos"] = pos
    expr_ast = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # 步骤 5: 消耗分号 token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected ';'")
    
    semicolon_token = tokens[pos]
    if semicolon_token["type"] != "SEMICOLON":
        raise SyntaxError(f"Expected ';', got '{semicolon_token['value']}'")
    
    pos += 1
    
    # 步骤 6: 更新 pos 并返回 VAR_DECL AST 节点
    parser_state["pos"] = pos
    
    var_decl_node: AST = {
        "type": "VAR_DECL",
        "children": [expr_ast],
        "value": {
            "keyword": keyword,
            "name": var_name
        },
        "line": line,
        "column": column
    }
    
    return var_decl_node

# === helper functions ===

# === OOP compatibility layer ===
