# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions to import

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
def _check_expression_types(node: AST, symbol_table: SymbolTable) -> None:
    """根据表达式操作符类型进行类型检查，记录类型错误到符号表。"""
    value = node.get("value")
    children = node.get("children", [])
    line = node.get("line", 0)
    column = node.get("column", 0)

    if value in ["+", "-", "*", "/"]:
        _check_arithmetic_op(children, symbol_table, line, column)
    elif value in ["&&", "||", "!"]:
        _check_logical_op(children, symbol_table, line, column)
    elif value in ["==", "!=", "<", ">", "<=", ">="]:
        _check_comparison_op(children, symbol_table, line, column)
    elif value == "=":
        _check_assignment_op(children, symbol_table, line, column)


# === helper functions ===
def _check_arithmetic_op(children: list, symbol_table: SymbolTable, line: int, column: int) -> None:
    """检查算术运算符：所有操作数必须为 int 类型。"""
    for child in children:
        data_type = child.get("data_type")
        if data_type != "int":
            _add_error(symbol_table, line, column,
                       f"算术运算符要求操作数为 int 类型，实际为 {data_type}")


def _check_logical_op(children: list, symbol_table: SymbolTable, line: int, column: int) -> None:
    """检查逻辑运算符：所有操作数必须为 int 类型（作为布尔值）。"""
    for child in children:
        data_type = child.get("data_type")
        if data_type != "int":
            _add_error(symbol_table, line, column,
                       f"逻辑运算符要求操作数为 int 类型，实际为 {data_type}")


def _check_comparison_op(children: list, symbol_table: SymbolTable, line: int, column: int) -> None:
    """检查比较运算符：所有操作数类型必须一致。"""
    if len(children) < 2:
        return
    first_type = children[0].get("data_type")
    for child in children[1:]:
        data_type = child.get("data_type")
        if data_type != first_type:
            _add_error(symbol_table, line, column,
                       f"比较运算符要求操作数类型一致，实际为 {first_type} 和 {data_type}")


def _check_assignment_op(children: list, symbol_table: SymbolTable, line: int, column: int) -> None:
    """检查赋值运算符：左值必须为已声明的 identifier，类型兼容。"""
    if len(children) < 2:
        return
    left = children[0]
    right = children[1]

    # 检查左值是否为 identifier
    if left.get("type") != "identifier":
        _add_error(symbol_table, line, column, "赋值运算符左值必须为 identifier")
        return

    var_name = left.get("value")
    variables = symbol_table.get("variables", {})

    # 检查左值是否已声明
    if var_name not in variables or not variables[var_name].get("is_declared", False):
        _add_error(symbol_table, line, column, f"变量 '{var_name}' 未声明")
        return

    # 检查类型兼容
    left_type = variables[var_name].get("data_type")
    right_type = right.get("data_type")
    if left_type != right_type:
        _add_error(symbol_table, line, column,
                   f"赋值类型不兼容：左值类型为 {left_type}，右值类型为 {right_type}")


def _add_error(symbol_table: SymbolTable, line: int, column: int, message: str) -> None:
    """向符号表的 errors 列表添加错误记录。"""
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    symbol_table["errors"].append({
        "type": "type_mismatch",
        "message": message,
        "line": line,
        "column": column,
        "node_type": "expression"
    })

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function node
