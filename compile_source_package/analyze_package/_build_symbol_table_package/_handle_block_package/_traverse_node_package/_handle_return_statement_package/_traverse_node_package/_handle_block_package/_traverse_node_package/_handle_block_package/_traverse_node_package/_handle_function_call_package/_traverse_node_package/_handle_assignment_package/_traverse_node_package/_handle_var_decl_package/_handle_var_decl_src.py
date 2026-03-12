# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "assignment", "var_decl", "if", "while", "block", "binary_op", "literal", "identifier", "expression", etc.)
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
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点，将变量信息注册到符号表。
    
    处理步骤：
    1. 从 node 中提取变量名、数据类型、行号、列号
    2. 检查变量是否已声明
    3. 如果已声明，记录重复声明错误
    4. 如果未声明，注册到符号表
    """
    # 从 node 中提取变量信息
    var_name = node.get("var_name")
    data_type = node.get("data_type")
    line = node.get("line")
    column = node.get("column")
    
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 初始化 variables 字典（如果不存在）
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 检查变量是否已声明
    if var_name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][var_name]
        if existing_var.get("is_declared", False):
            # 记录重复声明错误
            error = {
                "error": "duplicate declaration",
                "name": var_name,
                "line": line,
                "column": column
            }
            symbol_table["errors"].append(error)
            return
    
    # 注册新变量到符号表
    current_scope = symbol_table.get("current_scope", 0)
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
# Not needed for this internal function