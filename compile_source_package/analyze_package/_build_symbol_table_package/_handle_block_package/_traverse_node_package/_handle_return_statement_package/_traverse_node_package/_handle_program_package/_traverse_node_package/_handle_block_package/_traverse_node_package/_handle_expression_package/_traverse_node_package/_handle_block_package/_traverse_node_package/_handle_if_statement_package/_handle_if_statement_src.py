# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block

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
def _handle_if_statement(node: AST, symbol_table: SymbolTable) -> None:
    """处理 if 语句节点，递归处理条件表达式和分支块。"""
    children = node.get("children", [])
    
    for child in children:
        child_type = child.get("type", "")
        
        if child_type == "expression":
            _traverse_children_local(child, symbol_table)
        elif child_type == "block":
            _handle_block(child, symbol_table)
        else:
            _traverse_children_local(child, symbol_table)


# === helper functions ===
def _traverse_children_local(node: AST, symbol_table: SymbolTable) -> None:
    """本地辅助函数：递归遍历节点及其子节点。"""
    children = node.get("children", [])
    
    for child in children:
        child_type = child.get("type", "")
        
        if child_type == "block":
            _handle_block(child, symbol_table)
        else:
            _traverse_children_local(child, symbol_table)


# === OOP compatibility layer ===
