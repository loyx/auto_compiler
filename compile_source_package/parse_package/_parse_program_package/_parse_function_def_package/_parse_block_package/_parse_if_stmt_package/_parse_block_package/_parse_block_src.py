# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Deferred import to allow mocking in tests
_parse_statement = None

def _get_parse_statement():
    """Lazy import of _parse_statement to enable mocking."""
    global _parse_statement
    if _parse_statement is None:
        from ._parse_statement_package._parse_statement_src import _parse_statement as _stmt
        _parse_statement = _stmt
    return _parse_statement

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (IDENTIFIER, LBRACE, RBRACE, etc.)
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BLOCK, VAR_DECL, IF_STMT, etc.)
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
def _parse_block(parser_state: dict) -> dict:
    """解析语句块。返回 BLOCK 类型 AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否越界
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected block")
    
    current_token = tokens[pos]
    start_line = current_token["line"]
    start_column = current_token["column"]
    
    children = []
    
    # 判断是否是显式块（以 LBRACE 开始）
    if current_token["type"] == "LBRACE":
        # 消费 LBRACE
        parser_state["pos"] = pos + 1
        
        # 解析块内语句，直到遇到 RBRACE
        while parser_state["pos"] < len(tokens):
            current_token = tokens[parser_state["pos"]]
            
            # 遇到 RBRACE，结束块
            if current_token["type"] == "RBRACE":
                # 消费 RBRACE
                parser_state["pos"] += 1
                break
            
            # 解析一条语句
            statement_node = _get_parse_statement()(parser_state)
            children.append(statement_node)
        else:
            # 循环正常结束但未遇到 RBRACE
            raise SyntaxError("Missing closing brace '}' for block")
    else:
        # 隐式块：解析单条语句
        statement_node = _get_parse_statement()(parser_state)
        children.append(statement_node)
    
    # 构建 BLOCK AST 节点
    block_node = {
        "type": "BLOCK",
        "children": children,
        "line": start_line,
        "column": start_column
    }
    
    return block_node

# === helper functions ===
# No helper functions needed; logic is delegated to _parse_statement

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function