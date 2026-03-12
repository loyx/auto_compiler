# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_identifier_package._handle_identifier_src import _handle_identifier
from ._handle_literal_package._handle_literal_src import _handle_literal

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
def _handle_while(node: AST, symbol_table: SymbolTable) -> None:
    """处理 while 循环节点：遍历条件表达式和循环体，管理作用域。"""
    children = node.get("children", [])
    
    if len(children) != 2:
        _record_error(symbol_table, "while 语句必须包含条件表达式和循环体", node)
        return
    
    condition_node = children[0]
    body_node = children[1]
    
    _handle_condition(condition_node, symbol_table)
    
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    symbol_table["current_scope"] += 1
    
    try:
        _handle_block(body_node, symbol_table)
    finally:
        symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
def _handle_condition(node: AST, symbol_table: SymbolTable) -> None:
    """根据节点类型调度对应的 handler 处理条件表达式。"""
    node_type = node.get("type", "")
    
    if node_type == "binary_op":
        _handle_binary_op(node, symbol_table)
    elif node_type == "identifier":
        _handle_identifier(node, symbol_table)
    elif node_type == "literal":
        _handle_literal(node, symbol_table)
    else:
        _record_error(symbol_table, f"while 条件表达式不支持的节点类型：{node_type}", node)

def _record_error(symbol_table: SymbolTable, message: str, node: AST) -> None:
    """记录错误到符号表。"""
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    symbol_table["errors"].append({
        "type": "invalid_while_condition",
        "message": message,
        "line": node.get("line", "?"),
        "column": node.get("column", "?")
    })

# === OOP compatibility layer ===
