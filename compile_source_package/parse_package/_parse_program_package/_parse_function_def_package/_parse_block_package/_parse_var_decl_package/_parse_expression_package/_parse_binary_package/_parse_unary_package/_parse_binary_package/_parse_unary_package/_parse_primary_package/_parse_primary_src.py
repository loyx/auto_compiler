# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (IDENTIFIER, NUMBER, STRING, BOOL, LPAREN, RPAREN, etc.)
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (IDENTIFIER, LITERAL, BINARY_OP, UNARY_OP, etc.)
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
def _parse_primary(parser_state: ParserState) -> AST:
    """
    解析基础表达式（标识符、字面量、括号表达式等）。
    输入：parser_state（ParserState 类型）。
    处理：解析基础表达式并消耗相应 token。
    副作用：直接修改 parser_state["pos"] 消耗 token。
    返回：AST 节点（Dict）。
    异常：遇到无效 token 时抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 检查当前位置是否有效
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input while parsing primary expression")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    token_line = token.get("line", 0)
    token_column = token.get("column", 0)
    
    # 根据 token 类型分发处理
    if token_type == "IDENTIFIER":
        # 标识符节点
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    
    elif token_type == "NUMBER":
        # 数字字面量节点
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": {"type": "number", "data": token_value},
            "line": token_line,
            "column": token_column
        }
    
    elif token_type == "STRING":
        # 字符串字面量节点
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": {"type": "string", "data": token_value},
            "line": token_line,
            "column": token_column
        }
    
    elif token_type == "BOOL":
        # 布尔字面量节点
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": {"type": "bool", "data": token_value},
            "line": token_line,
            "column": token_column
        }
    
    elif token_type == "LPAREN":
        # 括号表达式：消耗 LPAREN，解析内部表达式，消耗 RPAREN
        parser_state["pos"] += 1  # 消耗 LPAREN
        
        # 解析括号内的完整表达式
        inner_ast = _parse_expression(parser_state)
        
        # 检查并消耗匹配的 RPAREN
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens):
            raise SyntaxError(f"{filename}:{token_line}:{token_column}: Missing closing parenthesis")
        
        closing_token = tokens[new_pos]
        if closing_token["type"] != "RPAREN":
            raise SyntaxError(
                f"{filename}:{closing_token.get('line', token_line)}:{closing_token.get('column', token_column)}: "
                f"Expected ')' but found '{closing_token['value']}'"
            )
        
        parser_state["pos"] += 1  # 消耗 RPAREN
        return inner_ast
    
    else:
        # 无法识别的 token 类型
        raise SyntaxError(
            f"{filename}:{token_line}:{token_column}: "
            f"Unexpected token '{token_value}' of type '{token_type}' in primary expression"
        )


# === helper functions ===
# (No helper functions needed - logic is straightforward)


# === OOP compatibility layer ===
# (Not needed for this parser function node)
