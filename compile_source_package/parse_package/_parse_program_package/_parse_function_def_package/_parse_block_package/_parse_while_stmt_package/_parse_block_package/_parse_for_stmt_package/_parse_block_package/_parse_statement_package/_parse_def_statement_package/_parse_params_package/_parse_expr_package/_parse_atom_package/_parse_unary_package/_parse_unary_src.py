# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_atom_package._parse_atom_src import _parse_atom

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
def _parse_unary(parser_state: ParserState, token: Token) -> AST:
    """
    解析一元运算表达式（MINUS/NOT），递归解析操作数并返回 UNOP AST 节点。
    
    Args:
        parser_state: 解析器状态，pos 指向一元运算符 token
        token: 当前一元运算符 token（type 必须是 MINUS 或 NOT）
    
    Returns:
        UNOP AST 节点，包含运算符和操作数
    """
    # 根据 token type 确定运算符
    if token["type"] == "MINUS":
        op = "-"
    elif token["type"] == "NOT":
        op = "not"
    else:
        raise ValueError(f"Invalid unary operator token type: {token['type']}")
    
    # 更新 pos 跳过运算符 token
    parser_state["pos"] += 1
    
    # 递归解析操作数
    operand_ast = _parse_atom(parser_state)
    
    # 构建 UNOP AST 节点
    return {
        "type": "UNOP",
        "op": op,
        "line": token["line"],
        "column": token["column"],
        "children": [operand_ast]
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
