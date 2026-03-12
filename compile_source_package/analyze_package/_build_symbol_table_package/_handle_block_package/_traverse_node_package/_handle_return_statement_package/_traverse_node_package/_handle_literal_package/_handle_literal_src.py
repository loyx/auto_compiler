# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple handler

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "literal")
#   "children": list,        # 子节点列表
#   "value": Any,            # 字面量的值 (如 42, 'a', "hello")
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
    处理 literal 类型节点（字面量）。
    
    职责：
    1. 提取字面量的值和类型
    2. 推断缺失的 data_type
    3. 验证字面量合法性
    4. 记录错误到符号表
    """
    value = node.get("value")
    data_type = node.get("data_type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 推断数据类型
    if data_type is None and value is not None:
        data_type = _infer_data_type(value)
        node["data_type"] = data_type
    
    # 验证字面量合法性
    is_valid = _validate_literal(value, data_type, line, column, symbol_table)
    
    return None

# === helper functions ===
def _infer_data_type(value: Any) -> str:
    """
    根据值推断数据类型。
    
    规则：
    - bool 类型 -> "unknown" (先检查，因为 bool 是 int 的子类)
    - int 类型 -> "int"
    - 单字符字符串 -> "char"
    - 多字符字符串 -> "string"
    - 其他 -> "unknown"
    """
    if isinstance(value, bool):
        return "unknown"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, str):
        if len(value) == 1:
            return "char"
        else:
            return "string"
    else:
        return "unknown"

def _validate_literal(value: Any, data_type: str, line: int, column: int, symbol_table: SymbolTable) -> bool:
    """
    验证字面量值的合法性。
    
    验证规则：
    - int: 检查是否为整数且在有效范围内 (-2147483648 到 2147483647)
    - char: 检查是否为单个字符
    - string: 字符串字面量，通常总是合法
    
    如果无效，记录错误到 symbol_table["errors"]
    """
    if value is None:
        _record_error(symbol_table, f"Invalid literal value 'None' at line {line}, column {column}")
        return False
    
    if data_type == "int":
        if not isinstance(value, int):
            _record_error(symbol_table, f"Invalid literal value '{value}' at line {line}, column {column}")
            return False
        # 检查整数范围 (32-bit signed integer)
        if value < -2147483648 or value > 2147483647:
            _record_error(symbol_table, f"Integer literal {value} out of range at line {line}, column {column}")
            return False
    
    elif data_type == "char":
        if not isinstance(value, str) or len(value) != 1:
            _record_error(symbol_table, f"Invalid char literal '{value}' at line {line}, column {column}")
            return False
    
    return True

def _record_error(symbol_table: SymbolTable, error_message: str) -> None:
    """记录错误到符号表的 errors 列表中。"""
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    symbol_table["errors"].append(error_message)

# === OOP compatibility layer ===
# Not needed for this helper function
