# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_expression_statement_package._handle_expression_statement_src import _handle_expression_statement
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,                 # 节点类型标识（必备字段）
#   "name": str,                 # 函数名/节点名
#   "params": list,              # 参数列表
#   "body": AST,                 # 函数体
#   "return_type": str,          # 返回类型
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归遍历 AST 节点，根据节点类型分发到对应的 handler 函数。
    
    输入：任意 AST 节点和符号表
    处理：根据节点类型调用对应 handler，未知类型递归遍历子节点
    副作用：通过 handler 函数原地修改 symbol_table
    """
    node_type = node.get("type")
    
    # 根据节点类型分发到对应 handler
    if node_type == "expression_statement":
        _handle_expression_statement(node, symbol_table)
    elif node_type == "function_declaration":
        _handle_function_declaration(node, symbol_table)
    elif node_type == "variable_declaration":
        _handle_variable_declaration(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if_statement":
        _handle_if_statement(node, symbol_table)
    elif node_type == "return_statement":
        _handle_return_statement(node, symbol_table)
    else:
        # 未知类型：递归遍历所有 AST 子节点
        _traverse_children(node, symbol_table)

# === helper functions ===
def _traverse_children(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归遍历节点的所有 AST 类型子字段。
    
    遍历规则：
    - 值为 Dict 且包含 "type" 字段 → 递归调用 _traverse_node
    - 值为 List → 遍历列表中每个元素，若为 AST 节点则递归
    """
    for key, value in node.items():
        if isinstance(value, dict) and "type" in value:
            _traverse_node(value, symbol_table)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "type" in item:
                    _traverse_node(item, symbol_table)

# === OOP compatibility layer ===
# 本函数为纯遍历逻辑，不需要 OOP wrapper
