# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_break_package._handle_break_src import _handle_break
from ._handle_continue_package._handle_continue_src import _handle_continue
from ._handle_return_package._handle_return_src import _handle_return
from ._handle_var_package._handle_var_src import _handle_var
from ._handle_call_package._handle_call_src import _handle_call
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "break", "continue", "return", "var", "call", "binary_op", "literal", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "condition": AST,        # while/if 节点的条件表达式 (可选)
#   "body": AST              # while/if/func 节点的循环体/函数体 (可选)
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
    """
    遍历 AST 节点并根据节点类型分发到对应的处理函数。
    
    输入：任意 AST 节点和符号表
    处理：根据 node["type"] 调用相应的 handler 函数
    副作用：可能修改 symbol_table
    异常：不抛出异常，错误记录在 symbol_table["errors"] 中
    """
    node_type = node.get("type", "")
    
    if node_type == "block":
        # 代码块：遍历所有子节点
        children = node.get("children", [])
        for child in children:
            _traverse_node(child, symbol_table)
    
    elif node_type == "var_decl":
        _handle_var_decl(node, symbol_table)
    
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    
    elif node_type == "if":
        _handle_if(node, symbol_table)
    
    elif node_type == "while":
        _handle_while(node, symbol_table)
    
    elif node_type == "break":
        _handle_break(node, symbol_table)
    
    elif node_type == "continue":
        _handle_continue(node, symbol_table)
    
    elif node_type == "return":
        _handle_return(node, symbol_table)
    
    elif node_type == "var":
        _handle_var(node, symbol_table)
    
    elif node_type == "call":
        _handle_call(node, symbol_table)
    
    elif node_type == "binary_op":
        _handle_binary_op(node, symbol_table)
    
    elif node_type == "literal":
        # 字面量：无需特殊处理
        pass
    
    else:
        # 未知节点类型：记录错误
        line = node.get("line", "unknown")
        column = node.get("column", "unknown")
        error_msg = f"Unknown node type '{node_type}' at line {line}, column {column}"
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append(error_msg)


# === helper functions ===
# No helper functions needed - all logic delegated to handlers

# === OOP compatibility layer ===
# Not needed for this internal traversal function
