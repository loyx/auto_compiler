# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions for this module

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

ErrorRecord = Dict[str, Any]
# ErrorRecord possible fields:
# {
#   "type": str,               # 错误类型 ("error")
#   "message": str,            # 错误描述
#   "line": int,               # 错误行号
#   "column": int              # 错误列号
# }

# === main function ===
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点。记录变量到符号表，检查重复声明。
    
    副作用：修改 symbol_table['variables']，可能添加错误到 symbol_table['errors']
    """
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 确保 variables 字典存在
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 获取变量名
    var_name = node.get("value")
    if var_name is None:
        _record_error(symbol_table, "Missing variable name in declaration", node)
        return
    
    # 获取数据类型
    data_type = node.get("data_type")
    if data_type is None:
        _record_error(symbol_table, "Missing data type in variable declaration", node)
        return
    
    # 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 检查变量是否已存在
    if var_name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][var_name]
        existing_scope = existing_var.get("scope_level", 0)
        
        # 如果在同一作用域，记录重复声明错误
        if existing_scope == current_scope:
            _record_error(
                symbol_table,
                f"Duplicate variable declaration: {var_name}",
                node
            )
            return
    
    # 记录变量到符号表
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": node.get("line", -1),
        "column": node.get("column", -1),
        "scope_level": current_scope
    }

# === helper functions ===
def _record_error(symbol_table: SymbolTable, message: str, node: AST) -> None:
    """
    记录错误到符号表的 errors 列表。
    
    副作用：修改 symbol_table['errors']
    """
    error: ErrorRecord = {
        "type": "error",
        "message": message,
        "line": node.get("line", -1),
        "column": node.get("column", -1)
    }
    symbol_table["errors"].append(error)

# === OOP compatibility layer ===
# Not required for this module (pure function node)
