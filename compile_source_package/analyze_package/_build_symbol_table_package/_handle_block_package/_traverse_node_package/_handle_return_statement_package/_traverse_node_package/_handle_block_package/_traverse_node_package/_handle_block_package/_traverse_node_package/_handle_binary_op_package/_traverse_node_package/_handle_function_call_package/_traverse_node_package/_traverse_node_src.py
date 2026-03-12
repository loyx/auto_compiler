# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_literal_package._handle_literal_src import _handle_literal
from ._handle_identifier_package._handle_identifier_src import _handle_identifier
from ._handle_default_package._handle_default_src import _handle_default

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", "function_call", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (如操作符、变量名、字面量值、函数名等)
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
    """
    递归遍历 AST 节点，根据节点类型分发到相应的处理函数。
    不抛出异常，所有错误记录到 symbol_table["errors"]。
    """
    if not isinstance(node, dict) or "type" not in node:
        _record_error(symbol_table, "Invalid AST node: missing 'type' field",
                      node.get("line", -1), node.get("column", -1))
        return
    
    node_type = node["type"]
    
    # 根据节点类型分发到对应处理函数
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
    elif node_type == "binary_op":
        _handle_binary_op(node, symbol_table)
    elif node_type == "literal":
        _handle_literal(node, symbol_table)
    elif node_type == "identifier":
        _handle_identifier(node, symbol_table)
    else:
        _handle_default(node, symbol_table)

# === helper functions ===
def _record_error(symbol_table: SymbolTable, message: str, line: int, column: int) -> None:
    """记录错误到符号表的 errors 列表。"""
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    symbol_table["errors"].append({
        "type": "error",
        "message": message,
        "line": line,
        "column": column
    })

# === OOP compatibility layer ===
# Not needed for this function node (semantic analysis helper)
