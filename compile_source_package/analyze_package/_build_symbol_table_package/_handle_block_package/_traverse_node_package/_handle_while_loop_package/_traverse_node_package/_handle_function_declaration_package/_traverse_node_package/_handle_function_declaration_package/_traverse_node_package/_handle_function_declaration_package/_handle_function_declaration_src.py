# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,
#   "params": list,
#   "body": AST,
#   "return_type": str,
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list
# }

FunctionEntry = Dict[str, Any]
# FunctionEntry possible fields:
# {
#   "name": str,
#   "return_type": str,
#   "params": list,
#   "scope": int,
#   "line": int,
#   "column": int
# }

# === main function ===
def _handle_function_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理函数声明节点，将函数信息注册到符号表中。
    
    从 node 中提取函数名、参数列表、返回类型、行号、列号，
    构建函数条目字典并存入 symbol_table["functions"][函数名]。
    
    副作用：修改 symbol_table["functions"] 字典
    """
    # 提取函数元数据
    func_name = node["name"]
    params = node["params"]
    return_type = node["return_type"]
    line = node["line"]
    column = node["column"]
    
    # 获取当前作用域
    current_scope = symbol_table["current_scope"]
    
    # 构建函数条目
    function_entry: FunctionEntry = {
        "name": func_name,
        "return_type": return_type,
        "params": params,
        "scope": current_scope,
        "line": line,
        "column": column
    }
    
    # 注册到符号表
    symbol_table["functions"][func_name] = function_entry

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node