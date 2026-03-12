# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this dispatch logic

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, ERROR, etc.)
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
def _handle_atom_token(token: Token, parser_state: ParserState) -> AST:
    """
    处理原子表达式 token 的分发逻辑（不包含 LPAREN 处理）。
    
    根据 token type 分发到对应的 AST 节点构建逻辑。
    消费 token（parser_state['pos'] += 1）并返回对应的 AST 节点。
    遇到不支持的 token 类型时设置 parser_state['error'] 并返回 ERROR 节点。
    """
    token_type = token.get("type", "")
    token_value = token.get("value", "")
    token_line = token.get("line", 0)
    token_column = token.get("column", 0)
    
    # 确保 parser_state['pos'] 存在
    if "pos" not in parser_state:
        parser_state["pos"] = 0
    
    # IDENTIFIER: 返回标识符节点
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "value": token_value,
            "children": [],
            "line": token_line,
            "column": token_column
        }
    
    # NUMBER/INTEGER: 返回字面量节点
    elif token_type in ("NUMBER", "INTEGER"):
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": token_value,
            "children": [],
            "line": token_line,
            "column": token_column
        }
    
    # STRING: 返回字符串字面量节点
    elif token_type == "STRING":
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": token_value,
            "children": [],
            "line": token_line,
            "column": token_column
        }
    
    # TRUE: 返回布尔字面量节点
    elif token_type == "TRUE":
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": True,
            "children": [],
            "line": token_line,
            "column": token_column
        }
    
    # FALSE: 返回布尔字面量节点
    elif token_type == "FALSE":
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": False,
            "children": [],
            "line": token_line,
            "column": token_column
        }
    
    # NONE/NULL: 返回空字面量节点
    elif token_type in ("NONE", "NULL"):
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": None,
            "children": [],
            "line": token_line,
            "column": token_column
        }
    
    # 其他：设置错误并返回 ERROR 节点
    else:
        parser_state["error"] = f"Unexpected token: {token_type}"
        return {
            "type": "ERROR",
            "value": token_value,
            "children": [],
            "line": token_line,
            "column": token_column
        }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser internal function
