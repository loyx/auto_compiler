# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

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
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点。
    
    从 AST 节点提取变量信息，检查是否重复声明，并注册到符号表。
    若变量已在当前作用域中声明，则记录错误到 symbol_table["errors"]。
    """
    var_name = node.get("value")
    data_type = node.get("data_type", "int")
    line = node.get("line", 0)
    column = node.get("column", 0)
    current_scope = symbol_table.get("current_scope", 0)
    
    variables = symbol_table.setdefault("variables", {})
    errors = symbol_table.setdefault("errors", [])
    
    if var_name in variables:
        existing_var = variables[var_name]
        if existing_var.get("scope_level") == current_scope:
            errors.append({
                "message": "变量重复声明",
                "line": line,
                "column": column,
                "var_name": var_name
            })
            return
    
    variables[var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }


# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function node
