# === std / third-party imports ===
from typing import Any, Dict, List, Optional

# === sub function imports ===
# No child functions needed for this simple validation logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
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
#   "errors": List[Dict],          # 错误列表（可选）
# }

ErrorInfo = Dict[str, Any]
# ErrorInfo possible fields:
# {
#   "error_type": str,       # 错误类型，如 "undeclared_variable"
#   "message": str,          # 错误消息
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "variable_name": str,    # 涉及的变量名
# }


# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 assignment 类型节点，验证被赋值变量是否已声明。
    
    如果变量未声明，在 symbol_table 中记录错误信息。
    如果变量已声明，可选验证类型匹配。
    静默处理，不抛异常。
    """
    # 1. 从 node 中提取被赋值的变量名
    var_name = _extract_variable_name(node)
    if var_name is None:
        return  # 无法提取变量名，静默返回
    
    # 2. 从 node 中提取行号、列号
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 3. 检查 symbol_table["variables"] 中是否存在该变量
    variables = symbol_table.get("variables", {})
    
    if var_name not in variables:
        # 4. 变量不存在，记录错误
        _record_undeclared_error(symbol_table, var_name, line, column)
    # 类型匹配验证暂不实现，可根据需要扩展


# === helper functions ===
def _extract_variable_name(node: AST) -> Optional[str]:
    """
    从 assignment node 中提取被赋值的变量名。
    
    尝试从 "target"、"name"、"value" 字段获取变量名。
    返回变量名字符串，如果无法提取则返回 None。
    """
    # 优先尝试 "target" 字段（常见于 assignment 节点）
    target = node.get("target")
    if isinstance(target, str):
        return target
    elif isinstance(target, dict):
        # target 可能是嵌套的 AST 节点
        return target.get("name") or target.get("value")
    
    # 尝试 "name" 字段
    name = node.get("name")
    if isinstance(name, str):
        return name
    
    # 尝试 "value" 字段（某些 AST 结构可能将变量名放在这里）
    value = node.get("value")
    if isinstance(value, str):
        return value
    elif isinstance(value, dict):
        return value.get("name") or value.get("value")
    
    return None


def _record_undeclared_error(
    symbol_table: SymbolTable, var_name: str, line: int, column: int
) -> None:
    """
    在 symbol_table 中记录未声明变量的错误信息。
    
    如果 symbol_table 中没有 errors 列表，则创建它。
    将错误信息添加到 errors 列表中。
    """
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    errors: List[ErrorInfo] = symbol_table["errors"]
    
    # 创建错误信息
    error_info: ErrorInfo = {
        "error_type": "undeclared_variable",
        "message": f"Variable '{var_name}' is used before declaration",
        "line": line,
        "column": column,
        "variable_name": var_name,
    }
    
    errors.append(error_info)


# === OOP compatibility layer ===
# Not needed for this helper function