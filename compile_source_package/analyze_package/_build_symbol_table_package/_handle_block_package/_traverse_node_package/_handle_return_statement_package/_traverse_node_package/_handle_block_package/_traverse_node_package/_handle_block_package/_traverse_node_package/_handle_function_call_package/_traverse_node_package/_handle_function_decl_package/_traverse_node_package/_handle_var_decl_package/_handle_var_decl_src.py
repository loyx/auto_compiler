# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_decl", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
#   "name": str,             # 变量名 (用于 var_decl 节点)
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
    处理变量声明节点。
    
    从 AST 节点中提取变量声明信息，检查是否重复声明，
    并注册到符号表中。
    """
    # 提取变量名 (优先使用 "name"，回退到 "value")
    var_name = node.get("name") or node.get("value")
    
    # 如果变量名为 None 或空，直接返回
    if var_name is None:
        return
    
    # 提取数据类型
    data_type = node.get("data_type", "int")
    
    # 提取位置信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 获取当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    
    # 初始化 errors 列表 (如果不存在)
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 初始化 variables 字典 (如果不存在)
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 检查变量是否已在当前作用域声明
    if var_name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][var_name]
        if existing_var.get("scope_level") == current_scope:
            # 同一作用域内重复声明，记录错误
            error_msg = f"Variable '{var_name}' already declared at line {existing_var.get('line', 0)}"
            symbol_table["errors"].append({
                "type": "duplicate_declaration",
                "message": error_msg,
                "line": line,
                "column": column,
                "variable": var_name
            })
            return
    
    # 注册变量到符号表
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
