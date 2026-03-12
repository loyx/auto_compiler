# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Delayed import to avoid circular dependency and enable testing with mocks
# _traverse_node is imported inside the function when needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "binary_op", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (如操作符、变量名、字面量值等)
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

# === main function ===
def _handle_binary_op(node: AST, symbol_table: SymbolTable) -> None:
    """处理二元操作表达式节点。"""
    # 延迟导入以避免循环依赖
    from ._traverse_node_package._traverse_node_src import _traverse_node
    
    # 获取操作符和操作数
    op = node.get("value", "")
    children = node.get("children", [])
    line = node.get("line", -1)
    column = node.get("column", -1)
    
    # 检查操作数数量
    if len(children) != 2:
        _record_error(symbol_table, f"Binary operator '{op}' requires exactly 2 operands, got {len(children)}", line, column)
        return
    
    left_operand = children[0]
    right_operand = children[1]
    
    # 递归遍历操作数
    _traverse_node(left_operand, symbol_table)
    _traverse_node(right_operand, symbol_table)
    
    # 获取操作数的数据类型
    left_type = left_operand.get("data_type") if left_operand else None
    right_type = right_operand.get("data_type") if right_operand else None
    
    # 根据操作符类型验证操作数类型兼容性
    if _is_arithmetic_op(op):
        _validate_arithmetic_operands(op, left_type, right_type, symbol_table, line, column)
    elif _is_comparison_op(op):
        _validate_comparison_operands(op, left_type, right_type, symbol_table, line, column)

# === helper functions ===
def _is_arithmetic_op(op: str) -> bool:
    """判断是否为算术操作符。"""
    return op in ["+", "-", "*", "/"]

def _is_comparison_op(op: str) -> bool:
    """判断是否为比较操作符。"""
    return op in ["==", "!=", "<", ">", "<=", ">="]

def _validate_arithmetic_operands(op: str, left_type: str, right_type: str, symbol_table: SymbolTable, line: int, column: int) -> None:
    """验证算术操作的操作数类型（要求均为 int）。"""
    if left_type != "int" or right_type != "int":
        _record_error(symbol_table, f"Invalid operand types for operator '{op}': arithmetic operations require int operands", line, column)

def _validate_comparison_operands(op: str, left_type: str, right_type: str, symbol_table: SymbolTable, line: int, column: int) -> None:
    """验证比较操作的操作数类型（要求类型一致）。"""
    if left_type != right_type:
        _record_error(symbol_table, f"Invalid operand types for operator '{op}': comparison operations require consistent types", line, column)

def _record_error(symbol_table: SymbolTable, message: str, line: int, column: int) -> None:
    """记录错误到符号表。"""
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    symbol_table["errors"].append({
        "type": "error",
        "message": message,
        "line": line,
        "column": column
    })

# === OOP compatibility layer ===
# No OOP wrapper needed for this handler function
