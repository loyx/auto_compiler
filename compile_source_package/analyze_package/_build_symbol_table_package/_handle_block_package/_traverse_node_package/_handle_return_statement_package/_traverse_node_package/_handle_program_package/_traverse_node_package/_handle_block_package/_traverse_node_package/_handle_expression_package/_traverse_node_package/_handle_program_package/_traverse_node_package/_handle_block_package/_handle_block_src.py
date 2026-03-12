# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple scope management operation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_block(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理代码块节点，进入新作用域层级。
    
    该函数负责在遇到 block 类型 AST 节点时更新符号表的作用域状态。
    子节点的遍历由 _traverse_node 自动处理，本函数仅负责作用域进入。
    
    Args:
        node: block 类型的 AST 节点
        symbol_table: 符号表（将被原地修改）
    
    Side effects:
        - symbol_table["current_scope"] 自增 1
        - symbol_table["scope_stack"] 压入新的作用域层级
    """
    # 进入新作用域：current_scope 自增
    symbol_table["current_scope"] += 1
    
    # 将新作用域压入栈
    symbol_table["scope_stack"].append(symbol_table["current_scope"])

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed: this is an internal helper function, not a framework entry point