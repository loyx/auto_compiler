# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# 注意：handler 函数在函数体内 import，避免循环依赖

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


# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归遍历 AST 节点，根据节点类型分发到对应 handler 函数。
    所有 handler 都原地修改 symbol_table。
    """
    # 在函数体内 import handler，避免与 handler 模块的循环依赖
    from ._handle_function_declaration_package._handle_function_declaration_src import _handle_function_declaration
    from ._handle_block_package._handle_block_src import _handle_block
    from ._handle_variable_declaration_package._handle_variable_declaration_src import _handle_variable_declaration
    from ._handle_assignment_package._handle_assignment_src import _handle_assignment
    from ._handle_if_statement_package._handle_if_statement_src import _handle_if_statement
    from ._handle_return_statement_package._handle_return_statement_src import _handle_return_statement

    node_type = node.get("type", "")

    # 分发到对应 handler
    if node_type == "function_declaration":
        _handle_function_declaration(node, symbol_table)
    elif node_type == "block":
        _handle_block(node, symbol_table)
    elif node_type == "variable_declaration":
        _handle_variable_declaration(node, symbol_table)
    elif node_type == "assignment":
        _handle_assignment(node, symbol_table)
    elif node_type == "if_statement":
        _handle_if_statement(node, symbol_table)
    elif node_type == "return_statement":
        _handle_return_statement(node, symbol_table)
    elif node_type == "program":
        # 程序根节点：直接遍历所有子节点
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)
    else:
        # 未知类型或其他类型（expression, literal, identifier, binary_operation 等）
        # 先检查是否为未知类型并记录错误
        known_types = {
            "program", "function_declaration", "block", "variable_declaration",
            "assignment", "if_statement", "return_statement", "expression",
            "literal", "identifier", "binary_operation"
        }
        if node_type not in known_types:
            # 记录未知节点类型错误
            if "errors" not in symbol_table:
                symbol_table["errors"] = []
            error_info = {
                "type": "unknown_node_type",
                "node_type": node_type,
                "line": node.get("line", -1),
                "column": node.get("column", -1)
            }
            symbol_table["errors"].append(error_info)

        # 默认行为：遍历 children（如果存在）
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)


# === helper functions ===
# 无 helper 函数，所有逻辑在主函数中

# === OOP compatibility layer ===
# 不需要 OOP wrapper，这是纯函数节点
