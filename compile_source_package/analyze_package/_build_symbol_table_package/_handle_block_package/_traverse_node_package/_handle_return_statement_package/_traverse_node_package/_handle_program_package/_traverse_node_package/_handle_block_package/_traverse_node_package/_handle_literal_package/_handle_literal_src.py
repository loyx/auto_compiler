# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions required for this simple literal handler

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "literal", "program", "function_declaration" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (字面量的具体值)
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
def _handle_literal(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 'literal' 类型节点。
    
    字面量节点表示常量值（整数、字符等），通常不需要修改符号表。
    此函数主要进行可选的类型验证和值范围检查。
    
    Args:
        node: literal 类型的 AST 节点
        symbol_table: 符号表（通常不被修改）
    
    Returns:
        None
    """
    # 验证节点类型
    if node.get("type") != "literal":
        return
    
    # 获取字面量的数据类型和值
    data_type = node.get("data_type")
    value = node.get("value")
    
    # 验证数据类型是否有效
    if not _is_valid_data_type(data_type):
        return
    
    # 验证字面量值是否在有效范围内
    _validate_literal_value(value, data_type, node, symbol_table)


# === helper functions ===
def _is_valid_data_type(data_type: Any) -> bool:
    """
    验证数据类型是否有效。
    
    Args:
        data_type: 数据类型字符串
    
    Returns:
        bool: 数据类型是否有效
    """
    valid_types = {"int", "char"}
    return data_type in valid_types if isinstance(data_type, str) else False


def _validate_literal_value(value: Any, data_type: str, node: AST, symbol_table: SymbolTable) -> None:
    """
    验证字面量值是否在有效范围内。
    
    Args:
        value: 字面量的值
        data_type: 数据类型 ("int" 或 "char")
        node: AST 节点（用于错误报告）
        symbol_table: 符号表（用于记录错误）
    
    Returns:
        None
    """
    if value is None:
        return
    
    # 根据数据类型进行验证
    if data_type == "int":
        _validate_int_literal(value, node, symbol_table)
    elif data_type == "char":
        _validate_char_literal(value, node, symbol_table)


def _validate_int_literal(value: Any, node: AST, symbol_table: SymbolTable) -> None:
    """
    验证整数字面量。
    
    Args:
        value: 整数值
        node: AST 节点
        symbol_table: 符号表
    
    Returns:
        None
    """
    # 检查是否为整数类型
    if not isinstance(value, int):
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "type": "type_error",
            "message": f"Expected int literal, got {type(value).__name__}",
            "line": node.get("line"),
            "column": node.get("column")
        })


def _validate_char_literal(value: Any, node: AST, symbol_table: SymbolTable) -> None:
    """
    验证字符字面量。
    
    Args:
        value: 字符值
        node: AST 节点
        symbol_table: 符号表
    
    Returns:
        None
    """
    # 检查是否为字符串且长度为 1
    if not isinstance(value, str) or len(value) != 1:
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "type": "type_error",
            "message": f"Expected char literal (single character), got {repr(value)}",
            "line": node.get("line"),
            "column": node.get("column")
        })


# === OOP compatibility layer ===
# Not required for this helper function node