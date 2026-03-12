# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# only import child functions
from ._handle_program_package._handle_program_src import _handle_program
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_binary_expression_package._handle_binary_expression_src import _handle_binary_expression
from ._handle_unary_expression_package._handle_unary_expression_src import _handle_unary_expression
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement
from ._handle_literal_package._handle_literal_src import _handle_literal
from ._handle_identifier_package._handle_identifier_src import _handle_identifier

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # 变量表
#   "functions": Dict[str, Dict],  # 函数表
#   "current_scope": int,          # 当前作用域
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名
#   "errors": list                 # 错误列表
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点。根据节点类型分发到对应的 handler 函数。"""
    # 基本输入验证
    if not isinstance(node, dict) or not isinstance(symbol_table, dict):
        return
    
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 获取节点类型
    node_type = node.get("type")
    if not isinstance(node_type, str):
        _record_error(symbol_table, f"Missing or invalid node type: {node_type}", 
                     node.get("line"), node.get("column"))
        return
    
    # 类型到 handler 的映射
    HANDLER_MAP = {
        "program": _handle_program,
        "function_declaration": _handle_function_declaration,
        "block": _handle_block,
        "if_statement": _handle_if_statement,
        "variable_declaration": _handle_variable_declaration,
        "assignment": _handle_assignment,
        "binary_expression": _handle_binary_expression,
        "unary_expression": _handle_unary_expression,
        "function_call": _handle_function_call,
        "return_statement": _handle_return_statement,
        "literal": _handle_literal,
        "identifier": _handle_identifier,
    }
    
    # 查找并调用对应的 handler
    handler = HANDLER_MAP.get(node_type)
    if handler:
        try:
            handler(node, symbol_table)
        except Exception as e:
            _record_error(symbol_table, f"Handler error for '{node_type}': {e}", 
                         node.get("line"), node.get("column"))
    else:
        _record_error(symbol_table, f"Unknown AST node type: {node_type}", 
                     node.get("line"), node.get("column"))

# === helper functions ===
def _record_error(symbol_table: SymbolTable, message: str, line: Any, column: Any) -> None:
    """记录错误到 symbol_table 的 errors 列表。"""
    if not isinstance(symbol_table, dict):
        return
    
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    error_entry = {
        "message": message,
        "line": line if isinstance(line, int) else "unknown",
        "column": column if isinstance(column, int) else "unknown",
        "type": "unknown_node_type" if "Unknown AST node type" in message else "handler_error"
    }
    symbol_table["errors"].append(error_entry)

# === OOP compatibility layer ===
# 不需要 OOP wrapper，因为这是纯函数节点