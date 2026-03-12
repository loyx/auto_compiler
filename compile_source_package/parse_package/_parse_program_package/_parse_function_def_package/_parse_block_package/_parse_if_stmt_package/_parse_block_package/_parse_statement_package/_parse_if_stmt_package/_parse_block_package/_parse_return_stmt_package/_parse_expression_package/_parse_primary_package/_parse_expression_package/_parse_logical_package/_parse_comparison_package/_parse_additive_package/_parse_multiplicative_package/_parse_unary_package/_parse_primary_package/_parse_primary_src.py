# === std / third-party imports ===
from typing import Any, Dict

# === ADT defines ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]

# === main function ===
def _parse_primary(parser_state: ParserState) -> AST:
    """
    解析初级表达式（字面量、标识符、括号表达式）。
    这是表达式解析的最底层，处理最高优先级的元素。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected expression")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    token_line = token.get("line", 0)
    token_column = token.get("column", 0)
    
    # 处理数字字面量
    if token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        return {
            "type": "number",
            "value": int(token_value) if "." not in token_value else float(token_value),
            "line": token_line,
            "column": token_column
        }
    
    # 处理字符串字面量
    if token_type == "STRING":
        parser_state["pos"] = pos + 1
        return {
            "type": "string",
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    
    # 处理布尔字面量
    if token_type == "KEYWORD" and token_value in ["True", "False"]:
        parser_state["pos"] = pos + 1
        return {
            "type": "boolean",
            "value": token_value == "True",
            "line": token_line,
            "column": token_column
        }
    
    # 处理 None 字面量
    if token_type == "KEYWORD" and token_value == "None":
        parser_state["pos"] = pos + 1
        return {
            "type": "none",
            "value": None,
            "line": token_line,
            "column": token_column
        }
    
    # 处理标识符
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {
            "type": "identifier",
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    
    # 处理括号表达式
    if token_type == "LPAREN":
        parser_state["pos"] = pos + 1
        
        # 解析括号内的表达式（调用 _parse_logical 避免循环导入）
        # 注意：这里需要延迟导入以避免循环依赖
        expr_ast = _parse_logical_in_parens(parser_state)
        
        # 消耗右括号
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"{filename}:{token_line}:{token_column}: Unclosed parenthesis")
        
        rparen_token = tokens[parser_state["pos"]]
        if rparen_token["type"] != "RPAREN":
            raise SyntaxError(f"{filename}:{rparen_token['line']}:{rparen_token['column']}: Expected ')', got {rparen_token['value']}")
        
        parser_state["pos"] += 1
        return expr_ast
    
    # 未知 token 类型
    raise SyntaxError(f"{filename}:{token_line}:{token_column}: Unexpected token '{token_value}' ({token_type})")

def _parse_logical_in_parens(parser_state: ParserState) -> AST:
    """
    在括号内解析表达式，避免循环导入。
    直接调用 _parse_logical，因为它是最顶层的表达式解析函数。
    """
    # 延迟导入以避免循环依赖
    from ..._parse_logical_package._parse_logical_src import _parse_logical
    return _parse_logical(parser_state)

# === helper functions ===

# === OOP compatibility layer ===
