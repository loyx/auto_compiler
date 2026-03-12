# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this leaf node handler

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "literal", "block", "var_decl", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (字面量的实际值)
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
    处理字面量 AST 节点。
    
    字面量是基本值（整数、字符），无需特殊语义检查。
    仅做基本数据类型验证。
    
    Args:
        node: literal 类型的 AST 节点
        symbol_table: 符号表（此函数不修改）
    """
    # 字面量节点无需特殊处理
    # 可选：验证数据类型是否有效
    data_type = node.get("data_type", "")
    
    if data_type not in ("int", "char"):
        # 记录警告但不抛出异常
        errors = symbol_table.get("errors", [])
        if errors is not None:
            errors.append({
                "type": "warning",
                "message": f"Invalid data type '{data_type}' for literal",
                "line": node.get("line", 0),
                "column": node.get("column", 0)
            })
    
    # 字面量是叶子节点，无需进一步处理
    return None

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node