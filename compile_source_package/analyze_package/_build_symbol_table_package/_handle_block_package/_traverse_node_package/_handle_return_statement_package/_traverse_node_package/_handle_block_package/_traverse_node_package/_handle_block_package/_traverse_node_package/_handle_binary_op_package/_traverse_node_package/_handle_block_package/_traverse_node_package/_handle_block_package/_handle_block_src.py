# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", "literal", "identifier", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (如操作符、变量名、字面量值等)
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
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
def _handle_block(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 block 类型节点，管理作用域并递归遍历子节点。
    """
    # 检查 node 是否有 "children" 字段
    if "children" not in node:
        error_msg = f"Block node missing 'children' field at line {node.get('line', 'unknown')}, column {node.get('column', 'unknown')}"
        symbol_table.setdefault("errors", []).append(error_msg)
        return
    
    # 进入 block: 保存当前 scope 并增加 scope_level
    old_scope = symbol_table.get("current_scope", 0)
    symbol_table.setdefault("scope_stack", []).append(old_scope)
    symbol_table["current_scope"] = old_scope + 1
    
    # 遍历子节点
    for child_node in node["children"]:
        _traverse_node(child_node, symbol_table)
    
    # 退出 block: 恢复 scope
    scope_stack = symbol_table.get("scope_stack", [])
    if scope_stack:
        symbol_table["current_scope"] = scope_stack.pop()

# === helper functions ===
# (none needed for this simple implementation)

# === OOP compatibility layer ===
# (not needed for this function node)
