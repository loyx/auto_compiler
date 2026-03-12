# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# _traverse_node is the parent dispatcher, imported from parent module
from ._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "condition": AST,        # if 节点的条件表达式
#   "then_block": AST,       # if 节点的 then 分支块
#   "else_block": AST,       # if 节点的 else 分支块（可选）
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list,           # 作用域栈 (存储旧 scope 值)
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_if(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 if 类型节点（条件语句）。
    
    遍历 if 节点的三个组成部分：
    1. condition: 条件表达式
    2. then_block: then 分支块
    3. else_block: else 分支块（可选）
    
    副作用：递归遍历子节点，可能修改 symbol_table
    """
    # 遍历条件表达式
    condition = node.get("condition")
    if condition is not None:
        _traverse_node(condition, symbol_table)
    
    # 遍历 then 分支块
    then_block = node.get("then_block")
    if then_block is not None:
        _traverse_node(then_block, symbol_table)
    
    # 遍历 else 分支块（如果存在）
    else_block = node.get("else_block")
    if else_block is not None:
        _traverse_node(else_block, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this handler function
