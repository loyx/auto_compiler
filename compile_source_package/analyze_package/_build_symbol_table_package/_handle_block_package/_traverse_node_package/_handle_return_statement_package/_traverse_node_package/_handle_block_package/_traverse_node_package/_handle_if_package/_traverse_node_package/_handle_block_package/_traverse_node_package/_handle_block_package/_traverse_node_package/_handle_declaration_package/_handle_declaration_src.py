# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("block", "declaration", "assignment", "function_call", etc.)
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
def _handle_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 declaration 类型 AST 节点，将变量注册到符号表中。
    
    如果变量已存在，记录重复声明错误；否则添加变量信息。
    """
    # 初始化符号表必要字段
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 提取变量名（优先从 value 获取，其次从 name 获取）
    var_name = node.get("value") or node.get("name")
    if not var_name:
        return  # 无变量名，跳过处理
    
    # 提取数据类型（默认 "int"）
    data_type = node.get("data_type", "int")
    
    # 提取位置信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 获取当前作用域层级（默认 0）
    current_scope = symbol_table.get("current_scope", 0)
    
    # 检查变量是否已声明
    if var_name in symbol_table["variables"]:
        # 记录重复声明错误
        error_msg = f"Duplicate declaration of variable '{var_name}' at line {line}, column {column}"
        symbol_table["errors"].append({
            "type": "duplicate_declaration",
            "message": error_msg,
            "line": line,
            "column": column,
            "variable": var_name
        })
    else:
        # 注册新变量
        symbol_table["variables"][var_name] = {
            "data_type": data_type,
            "is_declared": True,
            "line": line,
            "column": column,
            "scope_level": current_scope
        }


# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
