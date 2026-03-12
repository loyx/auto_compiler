# === std / third-party imports ===
from typing import Any, Dict, Callable

# === sub function imports ===
from ._handle_program_package._handle_program_src import _handle_program
from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
from ._handle_block_package._handle_block_src import _handle_block
from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
from ._handle_assignment_package._handle_assignment_src import _handle_assignment
from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement
from ._handle_expression_package._handle_expression_src import _handle_expression
from ._handle_literal_package._handle_literal_src import _handle_literal
from ._handle_identifier_package._handle_identifier_src import _handle_identifier

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
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

HandlerFunc = Callable[[AST, SymbolTable], None]

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归遍历 AST 节点并根据类型分发到对应的 handler 函数。
    
    处理逻辑：
    1. 根据 node["type"] 字段判断节点类型
    2. 分发到对应的 handler 函数
    3. 如果节点有 children，递归调用 _traverse_node 处理每个子节点
    4. 如果节点类型未知，记录错误到 symbol_table["errors"] 并继续处理子节点
    """
    node_type = node.get("type")
    
    # Handler 映射表
    handler_map: Dict[str, HandlerFunc] = {
        "program": _handle_program,
        "function_declaration": _handle_function_declaration,
        "block": _handle_block,
        "variable_declaration": _handle_variable_declaration,
        "assignment": _handle_assignment,
        "if_statement": _handle_if_statement,
        "return_statement": _handle_return_statement,
        "expression": _handle_expression,
        "literal": _handle_literal,
        "identifier": _handle_identifier,
    }
    
    # 分发到对应 handler 或处理未知类型
    if node_type in handler_map:
        handler_map[node_type](node, symbol_table)
    else:
        # 记录未知类型错误
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "type": "unknown_node_type",
            "message": f"未知的 AST 节点类型：{node_type}",
            "line": node.get("line"),
            "column": node.get("column")
        })
    
    # 递归处理子节点
    if "children" in node and node["children"]:
        for child in node["children"]:
            _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node