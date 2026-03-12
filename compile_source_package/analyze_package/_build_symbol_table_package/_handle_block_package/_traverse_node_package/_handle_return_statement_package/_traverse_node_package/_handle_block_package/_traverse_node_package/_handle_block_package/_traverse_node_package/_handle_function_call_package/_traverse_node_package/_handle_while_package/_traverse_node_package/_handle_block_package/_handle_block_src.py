# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
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
    处理 block 类型节点：管理作用域边界。
    
    处理步骤：
    1. 保存当前作用域层级到 scope_stack
    2. 增加 current_scope 层级（进入新作用域）
    3. 遍历 node["children"] 中的所有子节点，对每个子节点调用 _traverse_node
    4. 恢复作用域层级（从 scope_stack 弹出）
    """
    # Step 1: Save current scope level
    current_scope = symbol_table.get("current_scope", 0)
    symbol_table.setdefault("scope_stack", []).append(current_scope)
    
    # Step 2: Enter new scope (increment level)
    symbol_table["current_scope"] = current_scope + 1
    
    # Step 3: Traverse all children nodes
    children = node.get("children", [])
    for child_node in children:
        _traverse_node(child_node, symbol_table)
    
    # Step 4: Exit scope (restore previous level)
    symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this internal function node
