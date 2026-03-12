# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "expression": Any,
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _handle_return_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理返回语句节点。
    
    处理逻辑：
    1. 从 node 中提取 expression 字段
    2. 如果 expression 是一个 AST 节点（包含 "type" 字段），递归调用 _traverse_node 处理
    3. 如果 expression 是字面量或 None，不做处理
    
    副作用：不修改符号表
    """
    expression = node.get("expression")
    
    # 如果 expression 是 AST 节点（包含 "type" 字段的 Dict），递归处理
    if isinstance(expression, dict) and "type" in expression:
        _traverse_node(expression, symbol_table)
    # 否则（字面量、None 或其他类型），不做处理

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this handler function