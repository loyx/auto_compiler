# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "literal", "identifier", "block", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (标识符名称或字面量值)
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

ErrorInfo = Dict[str, Any]
# ErrorInfo possible fields:
# {
#   "message": str,            # 错误消息
#   "line": int,               # 错误行号
#   "column": int,             # 错误列号
#   "error_type": str          # 错误类型代码
# }


# === main function ===
def _get_expression_type(node: AST, symbol_table: SymbolTable) -> Optional[str]:
    """
    获取表达式的类型。
    
    处理逻辑：
    1. 如果 node["type"] == "literal"：直接从 node["data_type"] 读取并返回类型
    2. 如果 node["type"] == "identifier"：从 symbol_table["variables"] 中查找变量，返回其 data_type
    3. 如果不支持的节点类型：记录错误并返回 None
    4. 如果必要字段缺失：记录错误并返回 None
    5. 如果标识符未声明：记录错误并返回 None
    
    返回值：
    - 成功：返回 "int" 或 "char"
    - 失败：返回 None
    """
    node_type = node.get("type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    if node_type == "literal":
        return _handle_literal(node, line, column, symbol_table)
    elif node_type == "identifier":
        return _handle_identifier(node, line, column, symbol_table)
    else:
        _record_error(
            symbol_table,
            "UNSUPPORTED_EXPRESSION",
            f"Unsupported expression type: {node_type}",
            line,
            column
        )
        return None


# === helper functions ===
def _handle_literal(node: AST, line: int, column: int, symbol_table: SymbolTable) -> Optional[str]:
    """处理字面量节点，返回其数据类型。"""
    data_type = node.get("data_type")
    
    if data_type is None:
        _record_error(
            symbol_table,
            "INVALID_LITERAL",
            "Literal node missing data_type field",
            line,
            column
        )
        return None
    
    return data_type


def _handle_identifier(node: AST, line: int, column: int, symbol_table: SymbolTable) -> Optional[str]:
    """处理标识符节点，从符号表查找变量类型。"""
    var_name = node.get("value")
    
    if var_name is None:
        _record_error(
            symbol_table,
            "INVALID_IDENTIFIER",
            "Identifier node missing value field",
            line,
            column
        )
        return None
    
    variables = symbol_table.get("variables", {})
    
    if var_name not in variables:
        _record_error(
            symbol_table,
            "UNDECLARED_VAR",
            f"Undeclared variable: {var_name}",
            line,
            column
        )
        return None
    
    var_info = variables[var_name]
    return var_info.get("data_type")


def _record_error(
    symbol_table: SymbolTable,
    error_type: str,
    message: str,
    line: int,
    column: int
) -> None:
    """记录错误到符号表的 errors 列表中。"""
    error_info: ErrorInfo = {
        "message": message,
        "line": line,
        "column": column,
        "error_type": error_type
    }
    
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    symbol_table["errors"].append(error_info)


# === OOP compatibility layer ===
# Not needed for this helper function node
