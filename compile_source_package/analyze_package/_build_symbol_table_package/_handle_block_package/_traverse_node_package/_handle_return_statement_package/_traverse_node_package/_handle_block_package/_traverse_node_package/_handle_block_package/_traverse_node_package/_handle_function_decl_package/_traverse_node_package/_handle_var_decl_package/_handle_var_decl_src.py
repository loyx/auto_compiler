# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this module

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

VarInfo = Dict[str, Any]
# VarInfo possible fields:
# {
#   "data_type": str,        # 变量类型 ("int" 或 "char")
#   "is_declared": bool,     # 是否已声明
#   "line": int,             # 声明行号
#   "column": int,           # 声明列号
#   "scope_level": int       # 作用域层级
# }

ErrorInfo = Dict[str, Any]
# ErrorInfo possible fields:
# {
#   "type": str,             # 错误类型
#   "message": str,          # 错误消息
#   "line": int,             # 错误行号
#   "column": int            # 错误列号
# }

# === main function ===
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点，将变量信息注册到符号表。
    
    处理逻辑：
    1. 从 node["value"] 获取变量名
    2. 从 node["data_type"] 获取数据类型（"int" 或 "char"）
    3. 从 node["line"] 和 node["column"] 获取位置信息
    4. 检查变量是否已在当前作用域声明
    5. 将变量信息注册到 symbol_table["variables"][var_name]
    6. 如果变量已在当前作用域声明，记录"重复变量声明"错误
    """
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 检查必要字段是否存在
    if "value" not in node:
        _record_error(symbol_table, "MISSING_FIELD", "变量声明缺少 value 字段", node.get("line", 0), node.get("column", 0))
        return
    
    if "data_type" not in node:
        _record_error(symbol_table, "MISSING_FIELD", "变量声明缺少 data_type 字段", node.get("line", 0), node.get("column", 0))
        return
    
    var_name = node["value"]
    data_type = node["data_type"]
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 验证数据类型有效性
    if data_type not in ("int", "char"):
        _record_error(symbol_table, "INVALID_TYPE", f"无效的数据类型：{data_type}", line, column)
        return
    
    # 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 初始化 variables 字典（如果不存在）
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 检查变量是否已在当前作用域声明
    if var_name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][var_name]
        if existing_var.get("scope_level") == current_scope:
            _record_error(symbol_table, "DUPLICATE_DECL", f"变量 '{var_name}' 已在当前作用域声明", line, column)
            return
    
    # 注册变量到符号表
    var_info: VarInfo = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }
    symbol_table["variables"][var_name] = var_info

# === helper functions ===
def _record_error(symbol_table: SymbolTable, error_type: str, message: str, line: int, column: int) -> None:
    """
    记录错误信息到符号表的 errors 列表。
    
    参数：
    - symbol_table: 符号表字典
    - error_type: 错误类型标识
    - message: 错误描述消息
    - line: 错误发生行号
    - column: 错误发生列号
    """
    error_info: ErrorInfo = {
        "type": error_type,
        "message": message,
        "line": line,
        "column": column
    }
    symbol_table["errors"].append(error_info)

# === OOP compatibility layer ===
# Not needed for this helper function module
