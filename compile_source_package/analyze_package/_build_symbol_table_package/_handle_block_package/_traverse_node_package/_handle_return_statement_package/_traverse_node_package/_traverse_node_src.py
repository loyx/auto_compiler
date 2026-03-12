# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_program_package._handle_program_src import _handle_program
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_expression_package._handle_expression_src import _handle_expression
from ._handle_identifier_package._handle_identifier_src import _handle_identifier
from ._handle_literal_package._handle_literal_src import _handle_literal
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_while_loop_package._handle_while_loop_src import _handle_while_loop
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "return_statement", "identifier", "literal", "assignment", "expression" 等)
#   "children": list,        # 子节点列表
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
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归遍历 AST 节点树，根据节点类型分发到对应的 handler 函数。
    
    输入：AST 节点和符号表
    处理：根据节点类型调用对应的 handler 函数，递归遍历 children
    副作用：可能修改 symbol_table 或收集错误
    异常：遇到无法处理的节点类型时记录警告
    """
    node_type = node.get("type", "")
    
    # 分发到对应的 handler 函数
    handler_map = {
        "program": _handle_program,
        "function_declaration": _handle_function_declaration,
        "function_call": _handle_function_call,
        "return_statement": _handle_return_statement,
        "assignment": _handle_assignment,
        "expression": _handle_expression,
        "identifier": _handle_identifier,
        "literal": _handle_literal,
        "block": _handle_block,
        "if_statement": _handle_if_statement,
        "while_loop": _handle_while_loop,
        "variable_declaration": _handle_variable_declaration,
    }
    
    handler = handler_map.get(node_type)
    
    if handler:
        handler(node, symbol_table)
    else:
        # 未知节点类型，记录警告并尝试遍历 children
        errors = symbol_table.get("errors", [])
        line = node.get("line", "?")
        column = node.get("column", "?")
        errors.append(f"Warning: Unknown node type '{node_type}' at line {line}, column {column}")
    
    # 递归遍历子节点（如果 handler 未处理 children）
    children = node.get("children", [])
    if children and node_type not in ["program", "block", "if_statement", "while_loop", "function_declaration"]:
        for child in children:
            _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed - all logic delegated to handler functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function node