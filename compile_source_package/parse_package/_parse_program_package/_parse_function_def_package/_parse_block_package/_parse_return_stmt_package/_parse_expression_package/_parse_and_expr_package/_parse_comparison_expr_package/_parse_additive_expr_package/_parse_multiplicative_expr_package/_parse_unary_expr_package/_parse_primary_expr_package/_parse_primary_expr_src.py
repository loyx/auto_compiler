# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions - this is a leaf node in the function dependency tree

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
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
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """
    解析初级表达式（标识符、字面量、括号表达式等）。
    
    算法：
    1. 检查当前 token 类型
    2. 如果是标识符（IDENTIFIER），创建 IDENTIFIER 节点并消费 token
    3. 如果是字面量（NUMBER, STRING, BOOLEAN, NULL 等），创建 LITERAL 节点并消费 token
    4. 如果是左括号（LPAREN），解析括号内的表达式，然后消费右括号
    5. 其他情况抛出语法错误
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否还有 token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing primary expression")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    token_value = current_token["value"]
    token_line = current_token["line"]
    token_column = current_token["column"]
    
    # 处理标识符
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {
            "type": "IDENTIFIER",
            "value": token_value,
            "line": token_line,
            "column": token_column,
            "children": []
        }
    
    # 处理字面量
    elif token_type in ("NUMBER", "STRING", "BOOLEAN", "NULL"):
        parser_state["pos"] = pos + 1
        return {
            "type": "LITERAL",
            "value": token_value,
            "literal_type": token_type,
            "line": token_line,
            "column": token_column,
            "children": []
        }
    
    # 处理括号表达式
    elif token_type == "LPAREN":
        # 消费左括号
        parser_state["pos"] = pos + 1
        
        # 注意：这里需要调用 parse_expression 来解析括号内的表达式
        # 但由于这是 leaf node，我们假设括号内的表达式已经由上层处理
        # 实际上这会形成 mutual recursion，需要在更高层协调
        # 这里我们抛出异常表示需要上层处理
        raise SyntaxError("Parenthesized expression requires expression parser (mutual recursion)")
    
    # 其他情况：语法错误
    else:
        raise SyntaxError(
            f"Unexpected token '{token_value}' ({token_type}) at line {token_line}, column {token_column}. "
            f"Expected primary expression (identifier, literal, or parenthesized expression)."
        )

# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# Not needed - this is a parser helper function, not a framework entry point
