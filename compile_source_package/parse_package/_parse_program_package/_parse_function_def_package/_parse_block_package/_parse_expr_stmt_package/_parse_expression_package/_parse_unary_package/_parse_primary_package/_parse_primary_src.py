# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token

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
def _parse_primary(parser_state: dict) -> dict:
    """
    解析基本表达式单元（标识符、字面量、括号表达式）。
    输入：parser_state（当前位置指向基本单元起始 token）
    输出：AST 节点
    副作用：原地修改 parser_state["pos"]
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 检查是否超出范围
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of expression at {filename}")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]
    
    # 1. 标识符 (IDENTIFIER)
    if token_type == "IDENTIFIER":
        _consume_token(parser_state)
        return {
            "type": "IDENTIFIER",
            "value": token_value,
            "line": line,
            "column": column
        }
    
    # 2. 数字字面量 (NUMBER)
    elif token_type == "NUMBER":
        _consume_token(parser_state)
        return {
            "type": "LITERAL",
            "value": int(token_value),
            "line": line,
            "column": column
        }
    
    # 3. 字符串字面量 (STRING)
    elif token_type == "STRING":
        _consume_token(parser_state)
        # 去掉引号
        stripped_value = token_value[1:-1] if len(token_value) >= 2 else token_value
        return {
            "type": "LITERAL",
            "value": stripped_value,
            "line": line,
            "column": column
        }
    
    # 4. 布尔字面量 (KEYWORD: true/false)
    elif token_type == "KEYWORD":
        if token_value in ("true", "false"):
            _consume_token(parser_state)
            return {
                "type": "LITERAL",
                "value": token_value == "true",
                "line": line,
                "column": column
            }
        else:
            raise SyntaxError(f"Unexpected token '{token_value}' at {filename}:{line}:{column}")
    
    # 5. 括号表达式
    elif token_type == "PUNCTUATION" and token_value == "(":
        from ..._parse_expression_src import _parse_expression
        _consume_token(parser_state)  # 消费左括号
        inner_ast = _parse_expression(parser_state)  # 解析内部表达式
        
        # 检查并消费右括号
        pos = parser_state["pos"]
        if pos >= len(tokens):
            raise SyntaxError(f"Missing closing parenthesis at {filename}:{line}:{column}")
        
        closing_token = tokens[pos]
        if closing_token["type"] != "PUNCTUATION" or closing_token["value"] != ")":
            raise SyntaxError(f"Missing closing parenthesis at {filename}:{line}:{column}")
        
        _consume_token(parser_state)  # 消费右括号
        return inner_ast
    
    # 无法识别的 token 类型
    else:
        raise SyntaxError(f"Unexpected token '{token_value}' at {filename}:{line}:{column}")


# === helper functions ===
# (No helper functions needed; all logic is in main function)

# === OOP compatibility layer ===
# (Not needed for this parser function node)
