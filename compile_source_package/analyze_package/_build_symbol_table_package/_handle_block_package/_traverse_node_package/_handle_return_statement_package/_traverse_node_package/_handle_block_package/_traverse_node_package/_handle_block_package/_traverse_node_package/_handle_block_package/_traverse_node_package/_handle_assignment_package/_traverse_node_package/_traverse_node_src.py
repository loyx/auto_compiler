# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_function_call_package._handle_function_call_src import _handle_function_call

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
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点，根据节点类型分发到对应的处理函数。"""
    node_type = node.get("type", "")
    
    # 分发到具体 handler
    if node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "var_decl":
        _handle_var_decl(node, symbol_table)
    elif node_type == "if":
        _handle_if(node, symbol_table)
    elif node_type == "while":
        _handle_while(node, symbol_table)
    elif node_type == "function_call":
        _handle_function_call(node, symbol_table)
    elif node_type == "block":
        # 遍历 block 中的所有子节点
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)
    elif node_type in ("literal", "binary_op", "unary_op", "identifier"):
        # 表达式节点，递归处理 children
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)
    elif node_type == "return":
        # return 语句，处理返回值表达式
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)
    elif node_type == "function_def":
        # 函数定义，处理参数和函数体
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)
    else:
        # 默认处理：遍历所有 children
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed - all logic is in main function

# === OOP compatibility layer ===
# Not needed for this function node
