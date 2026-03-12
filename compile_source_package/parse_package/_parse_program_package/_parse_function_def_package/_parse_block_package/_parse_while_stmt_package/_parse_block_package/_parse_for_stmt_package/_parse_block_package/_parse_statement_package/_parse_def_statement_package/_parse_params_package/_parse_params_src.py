# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expr_package._parse_expr_src import _parse_expr

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
def _parse_params(parser_state: ParserState) -> AST:
    """解析函数参数列表。从 LPAREN 后开始，到 RPAREN 结束。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    params_children = []
    first_param_line = None
    first_param_column = None
    
    while pos < len(tokens):
        token = tokens[pos]
        
        # 遇到 RPAREN 结束参数列表
        if token["type"] == "RPAREN":
            break
        
        # 解析参数
        if token["type"] == "IDENT":
            if first_param_line is None:
                first_param_line = token["line"]
                first_param_column = token["column"]
            
            param_name = token["value"]
            param_line = token["line"]
            param_column = token["column"]
            pos += 1
            
            # 构建参数 AST
            param_ast: AST = {
                "type": "PARAM",
                "line": param_line,
                "column": param_column,
                "children": [{"type": "NAME", "value": param_name, "line": param_line, "column": param_column}]
            }
            
            # 检查是否有默认值 (EQUALS)
            if pos < len(tokens) and tokens[pos]["type"] == "EQUALS":
                pos += 1  # 消费 EQUALS
                if pos >= len(tokens):
                    raise SyntaxError("Expected expression after '='")
                # 解析默认值表达式
                default_value_ast = _parse_expr(parser_state)
                # 更新 pos 为 _parse_expr 消费后的位置
                pos = parser_state["pos"]
                param_ast["children"].append(default_value_ast)
            
            params_children.append(param_ast)
            
            # 检查逗号或结束
            if pos < len(tokens):
                next_token = tokens[pos]
                if next_token["type"] == "COMMA":
                    pos += 1  # 消费 COMMA
                    # 检查逗号后是否有参数
                    if pos >= len(tokens) or tokens[pos]["type"] not in ("IDENT", "RPAREN"):
                        if pos < len(tokens) and tokens[pos]["type"] != "RPAREN":
                            raise SyntaxError("Expected parameter after ','")
                elif next_token["type"] != "RPAREN":
                    raise SyntaxError("Expected ',' or ')' after parameter")
        elif token["type"] == "COMMA":
            # 逗号前没有参数
            raise SyntaxError("Expected parameter before ','")
        else:
            raise SyntaxError(f"Expected parameter name, got {token['type']}")
    
    # 更新 parser_state pos
    parser_state["pos"] = pos
    
    # 构建 PARAMS AST
    result: AST = {
        "type": "PARAMS",
        "line": first_param_line if first_param_line is not None else 0,
        "column": first_param_column if first_param_column is not None else 0,
        "children": params_children
    }
    
    return result


# === helper functions ===


# === OOP compatibility layer ===
