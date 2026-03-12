# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_function_decl_package._handle_function_decl_src import _handle_function_decl
from ._handle_return_package._handle_return_src import _handle_return
from ._handle_expression_package._handle_expression_src import _handle_expression

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (必填，永不为空)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (可选)
#   "data_type": str,        # 类型信息 "int" 或 "char" (可选)
#   "line": int,             # 行号 (必填，最小为 0)
#   "column": int            # 列号 (必填，最小为 0)
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
    """递归遍历 AST 节点，根据类型分发到对应 handler。
    
    Args:
        node: AST 节点，必须包含 "type" 字段
        symbol_table: 符号表，用于记录变量、作用域和错误
    
    Returns:
        None
    
    Side Effects:
        修改 symbol_table（作用域变化、变量声明、错误记录等）
    """
    node_type = node.get("type")
    
    if node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "var_decl":
        _handle_var_decl(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if":
        _handle_if(node, symbol_table)
    elif node_type == "while":
        _handle_while(node, symbol_table)
    elif node_type == "function_call":
        _handle_function_call(node, symbol_table)
    elif node_type == "function_decl":
        _handle_function_decl(node, symbol_table)
    elif node_type == "return":
        _handle_return(node, symbol_table)
    elif node_type == "expression":
        _handle_expression(node, symbol_table)
    else:
        # 未知节点类型，记录错误
        symbol_table.setdefault("errors", []).append({
            "type": "unknown_node",
            "message": f"未知节点类型：{node_type}",
            "line": node.get("line", 0),
            "column": node.get("column", 0)
        })

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node
