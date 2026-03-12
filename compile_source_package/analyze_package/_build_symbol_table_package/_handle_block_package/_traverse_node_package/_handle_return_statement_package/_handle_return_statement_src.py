# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# Mock _traverse_node for unit testing purposes
def _traverse_node(node, symbol_table):
    """
    Stub implementation of _traverse_node for unit testing.
    In production, this would be imported from _traverse_node_package.
    """
    pass

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "return_statement", "identifier", "literal")
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
def _handle_return_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 return_statement 类型节点。
    验证返回值类型与函数返回类型是否匹配。
    """
    # 提取位置信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 获取返回值表达式节点
    return_expr = _extract_return_expression(node)
    
    # 如果有返回值表达式，递归遍历
    if return_expr is not None:
        _traverse_node(return_expr, symbol_table)
        
        # 验证返回类型
        _validate_return_type(return_expr, node, symbol_table, line, column)


# === helper functions ===
def _extract_return_expression(node: AST) -> Optional[AST]:
    """
    从 return_statement 节点中提取返回值表达式。
    返回值可能在 children 列表或 value 字段中。
    """
    # 优先从 children 中获取
    children = node.get("children", [])
    if children and isinstance(children, list):
        # 返回语句的第一个子节点通常是返回值表达式
        for child in children:
            if isinstance(child, dict) and child.get("type") != "void":
                return child
        # 如果没有找到非 void 的子节点，返回第一个
        if len(children) > 0:
            return children[0] if isinstance(children[0], dict) else None
    
    # 尝试从 value 字段获取
    value = node.get("value")
    if value is not None and isinstance(value, dict):
        return value
    
    return None


def _validate_return_type(
    return_expr: AST,
    node: AST,
    symbol_table: SymbolTable,
    line: int,
    column: int
) -> None:
    """
    验证返回值类型与当前函数返回类型是否匹配。
    """
    # 获取当前函数名
    current_function = symbol_table.get("current_function")
    if not current_function:
        return
    
    # 获取函数信息
    functions = symbol_table.get("functions", {})
    func_info = functions.get(current_function, {})
    expected_return_type = func_info.get("return_type")
    
    if not expected_return_type:
        return
    
    # 获取返回表达式的实际类型
    actual_type = return_expr.get("data_type")
    
    # 类型匹配检查
    if actual_type and expected_return_type:
        if actual_type != expected_return_type:
            # 记录类型不匹配错误
            error = {
                "type": "return_type_mismatch",
                "line": line,
                "column": column,
                "expected": expected_return_type,
                "actual": actual_type,
                "function": current_function
            }
            errors = symbol_table.setdefault("errors", [])
            errors.append(error)


# === OOP compatibility layer ===
# Not needed for this helper function node
