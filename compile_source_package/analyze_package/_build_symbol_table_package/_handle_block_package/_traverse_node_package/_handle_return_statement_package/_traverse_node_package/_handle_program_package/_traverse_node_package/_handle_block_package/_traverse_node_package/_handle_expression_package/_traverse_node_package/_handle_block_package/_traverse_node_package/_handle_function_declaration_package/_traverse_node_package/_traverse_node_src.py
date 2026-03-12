# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block", "parameter_list", "parameter" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "name": str,             # 名称 (用于 function_declaration, parameter 等)
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
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点并更新符号表。"""
    node_type = node.get("type", "")
    
    if node_type == "function_declaration":
        _handle_function_declaration(node, symbol_table)
    elif node_type == "variable_declaration":
        _handle_variable_declaration(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "program":
        _handle_program(node, symbol_table)
    # 其他类型节点跳过或递归处理 children
    
    # 对于有 children 的节点，递归遍历子节点
    if "children" in node and isinstance(node["children"], list):
        for child in node["children"]:
            _traverse_node(child, symbol_table)


# === helper functions ===
def _handle_block(node: AST, symbol_table: SymbolTable) -> None:
    """处理 block 节点：进入新作用域。"""
    symbol_table["current_scope"] = symbol_table.get("current_scope", 0) + 1
    symbol_table.setdefault("scope_stack", []).append(symbol_table["current_scope"])


def _handle_program(node: AST, symbol_table: SymbolTable) -> None:
    """处理 program 节点：初始化符号表。"""
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    if "errors" not in symbol_table:
        symbol_table["errors"] = []


# === OOP compatibility layer ===
