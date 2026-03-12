# === std / third-party imports ===
from typing import Any, Dict, List, Optional

# === sub function imports ===
from ._add_error_package._add_error_src import _add_error

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block", "expression" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (对于 expression 节点，存储操作符)
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
#   "errors": list                 # 错误列表
# }

# === main function ===
def _check_arithmetic_operator(operator: str, operand_types: List[Optional[str]], line: int, column: int, current_scope: int, symbol_table: SymbolTable, node: AST) -> None:
    """检查算术运算符的类型约束。"""
    # 规则 1: 操作数类型列表长度必须为 2
    if len(operand_types) != 2:
        return
    
    left_type, right_type = operand_types[0], operand_types[1]
    
    # 规则 2: 任一操作数类型为 None，直接返回（子节点类型未确定）
    if left_type is None or right_type is None:
        return
    
    # 规则 3: 检查 char 类型相关错误
    if left_type == "char" or right_type == "char":
        if left_type != right_type:
            # 类型不匹配：一个 int 一个 char
            _add_error(
                error_type="TYPE_MISMATCH",
                message="Type mismatch: cannot mix int and char in arithmetic operation",
                line=line,
                column=column,
                scope=current_scope,
                symbol_table=symbol_table
            )
        else:
            # 都是 char：不允许对 char 进行算术运算
            _add_error(
                error_type="TYPE_MISMATCH",
                message="Arithmetic operations on char type are not allowed",
                line=line,
                column=column,
                scope=current_scope,
                symbol_table=symbol_table
            )
        return
    
    # 规则 4: 两个操作数都是 int，设置节点数据类型
    if left_type == "int" and right_type == "int":
        node["data_type"] = "int"

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this utility function
