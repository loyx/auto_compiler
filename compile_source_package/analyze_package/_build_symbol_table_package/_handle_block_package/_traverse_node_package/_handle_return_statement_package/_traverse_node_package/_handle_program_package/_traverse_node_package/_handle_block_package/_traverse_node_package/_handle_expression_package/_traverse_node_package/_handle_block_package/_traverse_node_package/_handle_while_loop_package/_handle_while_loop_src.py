# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
#   "children": list,        # 子节点列表
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
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_while_loop(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 while 循环节点。
    
    遍历 node["children"] 查找条件表达式和循环体块，
    调用 _traverse_node 递归处理各子节点。
    符号表修改原地进行。
    """
    for child in node.get("children", []):
        if not isinstance(child, dict):
            continue
        
        child_type = child.get("type", "")
        
        # 条件表达式或循环体块都通过 _traverse_node 处理
        # block 类型自身会管理作用域，无需特殊处理
        _traverse_node(child, symbol_table)

# === helper functions ===

# === OOP compatibility layer ===
