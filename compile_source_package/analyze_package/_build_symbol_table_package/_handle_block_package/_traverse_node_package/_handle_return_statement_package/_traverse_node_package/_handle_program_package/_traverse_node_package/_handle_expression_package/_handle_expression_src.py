# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# 延迟导入以避免循环依赖
# from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block", "expression" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int,           # 列号
#   "operator": str,         # 操作符 (对于 expression 节点)
#   "operands": list,        # 操作数列表 (对于 expression 节点)
#   "left": AST,             # 左操作数 (对于二元表达式)
#   "right": AST,            # 右操作数 (对于二元表达式)
#   "name": str              # 变量名或函数名
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 [{"message": str, "line": int, "column": int, "type": str}]
# }

# === main function ===
def _handle_expression(node: AST, symbol_table: SymbolTable) -> None:
    """处理 expression 类型节点，验证操作数类型兼容性，检查变量/函数声明。"""
    line = node.get("line", 0)
    column = node.get("column", 0)
    operator = node.get("operator") or node.get("op") or node.get("type", "")
    
    # 递归处理所有子节点
    children = node.get("children") or node.get("operands") or []
    for child in children:
        if isinstance(child, dict):
            _traverse_node(child, symbol_table)
    
    # 处理左右操作数（二元表达式）
    left = node.get("left")
    right = node.get("right")
    if left and isinstance(left, dict):
        _traverse_node(left, symbol_table)
    if right and isinstance(right, dict):
        _traverse_node(right, symbol_table)
    
    # 检查操作数类型兼容性（二元运算符）
    binary_operators = {"+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "&&", "||"}
    if operator in binary_operators and left and right:
        left_type = _get_operand_type(left, symbol_table)
        right_type = _get_operand_type(right, symbol_table)
        if left_type and right_type and left_type != right_type:
            _add_error(symbol_table, "Operand type mismatch in expression", line, column, "operand_type_mismatch")
    
    # 检查变量引用
    if operator == "identifier" or node.get("type") == "variable":
        var_name = node.get("value") or node.get("name")
        if var_name:
            _check_variable_declared(var_name, symbol_table, line, column)
    
    # 检查函数调用
    if operator == "call" or node.get("type") == "function_call":
        func_name = node.get("value") or node.get("name")
        if func_name:
            _check_function_declared(func_name, symbol_table, line, column)


# === helper functions ===
def _get_operand_type(operand: Any, symbol_table: SymbolTable) -> str:
    """获取操作数的类型。"""
    if not isinstance(operand, dict):
        return operand.get("data_type") if isinstance(operand, dict) else None
    
    if operand.get("data_type"):
        return operand["data_type"]
    
    # 变量引用，从符号表查找
    var_name = operand.get("value") or operand.get("name")
    if var_name and var_name in symbol_table.get("variables", {}):
        return symbol_table["variables"][var_name].get("data_type")
    
    return None


def _check_variable_declared(var_name: str, symbol_table: SymbolTable, line: int, column: int) -> None:
    """检查变量是否已声明。"""
    variables = symbol_table.get("variables", {})
    if var_name not in variables:
        _add_error(symbol_table, f"Use of undeclared variable '{var_name}'", line, column, "undeclared_variable")


def _check_function_declared(func_name: str, symbol_table: SymbolTable, line: int, column: int) -> None:
    """检查函数是否已声明。"""
    functions = symbol_table.get("functions", {})
    if func_name not in functions:
        _add_error(symbol_table, f"Call to undeclared function '{func_name}'", line, column, "undeclared_function")


def _add_error(symbol_table: SymbolTable, message: str, line: int, column: int, error_type: str) -> None:
    """向符号表添加错误记录。"""
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    symbol_table["errors"].append({
        "message": message,
        "line": line,
        "column": column,
        "type": error_type
    })

# === OOP compatibility layer ===
# Not required for this helper function node
