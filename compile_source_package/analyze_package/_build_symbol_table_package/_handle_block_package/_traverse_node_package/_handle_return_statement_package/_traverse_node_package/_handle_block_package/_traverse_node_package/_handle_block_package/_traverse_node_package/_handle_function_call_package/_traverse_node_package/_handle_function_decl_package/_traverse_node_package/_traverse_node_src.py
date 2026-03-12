# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_return_package._handle_return_src import _handle_return
from ._traverse_children_package._traverse_children_src import _traverse_children

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_decl", etc.)
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
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点树，根据节点类型分发到相应处理逻辑。"""
    node_type = node.get("type", "")
    
    # 作用域管理：遇到 block 时进入新作用域
    if node_type == "block":
        old_scope = symbol_table.get("current_scope", 0)
        symbol_table["current_scope"] = old_scope + 1
        if "scope_stack" not in symbol_table:
            symbol_table["scope_stack"] = []
        symbol_table["scope_stack"].append(old_scope)
        
        children = node.get("children", [])
        _traverse_children(children, symbol_table)
        
        # 离开 block 时恢复作用域
        if symbol_table["scope_stack"]:
            symbol_table["current_scope"] = symbol_table["scope_stack"].pop()
        else:
            symbol_table["current_scope"] = 0
        return
    
    # 根据节点类型分发到相应处理函数
    if node_type == "var_decl":
        _handle_var_decl(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if":
        _handle_if(node, symbol_table)
    elif node_type == "while":
        _handle_while(node, symbol_table)
    elif node_type == "function_call":
        _handle_function_call(node, symbol_table)
    elif node_type == "return":
        _handle_return(node, symbol_table)
    else:
        # 其他类型：递归遍历子节点
        children = node.get("children", [])
        _traverse_children(children, symbol_table)

# === helper functions ===
# (helper functions are delegated to sub-function modules)

# === OOP compatibility layer ===
# Not required for this function node (internal traversal logic)
