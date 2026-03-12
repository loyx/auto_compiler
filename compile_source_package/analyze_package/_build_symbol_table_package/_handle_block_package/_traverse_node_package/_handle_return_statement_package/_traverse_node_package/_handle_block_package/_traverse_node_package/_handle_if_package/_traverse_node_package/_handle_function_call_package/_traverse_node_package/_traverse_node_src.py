# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_var_decl_package._handle_var_decl_src import _handle_var_decl
from ._handle_assignment_package._handle_assignment_src import _handle_assignment

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", "literal", "identifier", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "name": str,             # 名称 (function_call / identifier 节点使用)
#   "value": Any,            # 节点值 (literal 节点使用)
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
#   "errors": list                 # 错误列表 (保证已初始化为 [])
# }


# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点进行语义分析。"""
    node_type = node.get("type", "")
    line = node.get("line", 0)
    column = node.get("column", 0)

    if node_type == "block":
        children = node.get("children", [])
        for child in children:
            _traverse_node(child, symbol_table)

    elif node_type == "var_decl":
        _handle_var_decl(node, symbol_table)

    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)

    elif node_type == "if":
        condition = node.get("condition")
        if condition:
            _traverse_node(condition, symbol_table)
        body = node.get("body", [])
        for child in body:
            _traverse_node(child, symbol_table)

    elif node_type == "while":
        condition = node.get("condition")
        if condition:
            _traverse_node(condition, symbol_table)
        body = node.get("body", [])
        for child in body:
            _traverse_node(child, symbol_table)

    elif node_type == "function_call":
        _handle_function_call(node, symbol_table)

    elif node_type == "literal":
        pass  # 字面量无需特殊处理

    elif node_type == "identifier":
        name = node.get("name")
        if name:
            variables = symbol_table.get("variables", {})
            if name not in variables:
                symbol_table["errors"].append({
                    "type": "error",
                    "message": f"Undefined variable: {name}",
                    "line": line,
                    "column": column
                })

    else:
        children = node.get("children", [])
        for child in children:
            _traverse_node(child, symbol_table)


# === helper functions ===
# No helper functions needed; all logic is in main function.

# === OOP compatibility layer ===
# Not needed for this function node.