# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
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
#   "scope_stack": list,           # 作用域栈 (存储旧 scope 值)
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_literal(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理字面量节点，验证字面量类型合法性。
    
    验证逻辑：
    1. 检查 data_type 是否为 "int" 或 "char"
    2. 对于 "int" 类型，验证值是否为整数或在整数范围内
    3. 对于 "char" 类型，验证值是否为单个字符
    4. 错误记录到 symbol_table['errors']，不抛出异常
    """
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 获取节点信息
    data_type = node.get("data_type", "")
    value = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 验证数据类型是否合法
    if data_type not in ("int", "char"):
        error_msg = f"Invalid literal type '{data_type}' at line {line}, column {column}"
        symbol_table["errors"].append(error_msg)
        return
    
    # 根据类型验证值
    if data_type == "int":
        _validate_int_literal(value, line, column, symbol_table)
    elif data_type == "char":
        _validate_char_literal(value, line, column, symbol_table)

# === helper functions ===
def _validate_int_literal(value: Any, line: int, column: int, symbol_table: SymbolTable) -> None:
    """验证整数字面量的合法性。"""
    # 检查是否为整数类型
    if isinstance(value, bool):
        # bool 是 int 的子类，需要排除
        error_msg = f"Invalid int literal value (boolean) at line {line}, column {column}"
        symbol_table["errors"].append(error_msg)
    elif not isinstance(value, int):
        # 尝试检查是否为字符串形式的整数
        if isinstance(value, str):
            try:
                int(value)
                return  # 字符串形式的整数是合法的
            except ValueError:
                pass
        error_msg = f"Invalid int literal value '{value}' at line {line}, column {column}"
        symbol_table["errors"].append(error_msg)
    # 可选：检查整数范围（Python 整数无固定范围，可根据需要添加）
    # elif value < -2147483648 or value > 2147483647:
    #     error_msg = f"Int literal value {value} out of range at line {line}, column {column}"
    #     symbol_table["errors"].append(error_msg)

def _validate_char_literal(value: Any, line: int, column: int, symbol_table: SymbolTable) -> None:
    """验证字符字面量的合法性。"""
    # 检查是否为字符串且长度为 1
    if not isinstance(value, str):
        error_msg = f"Invalid char literal value (not a string) '{value}' at line {line}, column {column}"
        symbol_table["errors"].append(error_msg)
    elif len(value) != 1:
        error_msg = f"Invalid char literal value (length={len(value)}) '{value}' at line {line}, column {column}"
        symbol_table["errors"].append(error_msg)

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function node
