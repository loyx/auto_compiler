# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_function_decl_package._handle_function_decl_src import _handle_function_decl
from ._handle_return_package._handle_return_src import _handle_return
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_identifier_package._handle_identifier_src import _handle_identifier
from ._handle_literal_package._handle_literal_src import _handle_literal

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
def _handle_while(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理循环语句节点。
    
    验证 while 节点结构，遍历条件表达式和循环体。
    错误记录到 symbol_table["errors"]，不抛出异常。
    """
    line = node.get("line", 0)
    column = node.get("column", 0)
    children = node.get("children", [])
    
    # 验证 children 数量
    if len(children) < 2:
        errors = symbol_table.setdefault("errors", [])
        errors.append(f"While statement missing condition or body at line {line}, column {column}")
        return
    
    # 遍历条件表达式 (children[0])
    _traverse_node(children[0], symbol_table)
    
    # 遍历循环体 (children[1])
    _traverse_node(children[1], symbol_table)


# === helper functions ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    统一分发入口，根据节点类型路由到对应的 handler。
    
    本函数作为当前模块的分发器，调用各类型节点的 handler。
    """
    node_type = node.get("type", "")
    
    # 路由到对应的 handler
    if node_type == "while":
        _handle_while(node, symbol_table)
    elif node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "var_decl":
        _handle_var_decl(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if":
        _handle_if(node, symbol_table)
    elif node_type == "function_call":
        _handle_function_call(node, symbol_table)
    elif node_type == "function_decl":
        _handle_function_decl(node, symbol_table)
    elif node_type == "return":
        _handle_return(node, symbol_table)
    elif node_type == "binary_op":
        _handle_binary_op(node, symbol_table)
    elif node_type == "identifier":
        _handle_identifier(node, symbol_table)
    elif node_type == "literal":
        _handle_literal(node, symbol_table)
