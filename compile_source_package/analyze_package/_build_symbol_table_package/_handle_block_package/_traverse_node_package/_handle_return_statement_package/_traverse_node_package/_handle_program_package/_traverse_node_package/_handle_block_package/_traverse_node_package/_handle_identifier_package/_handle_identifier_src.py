# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple validation logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block", "identifier" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (identifier 节点中为标识符名称字符串)
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
def _handle_identifier(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 'identifier' 类型节点，验证标识符已声明。
    
    输入：identifier 类型的 AST 节点和符号表
    处理：检查 node['value'] 是否在 variables 或 functions 中
    副作用：如果未声明，记录错误到 symbol_table["errors"]
    异常：无（错误通过 symbol_table 返回）
    """
    # 从节点获取标识符名称
    identifier_name = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 检查是否在 variables 中声明
    variables = symbol_table.get("variables", {})
    if identifier_name in variables:
        return  # 已声明为变量，验证通过
    
    # 检查是否在 functions 中声明
    functions = symbol_table.get("functions", {})
    if identifier_name in functions:
        return  # 已声明为函数，验证通过
    
    # 都未找到，记录未声明错误
    error_message = f"未声明的标识符 '{identifier_name}' at line {line}, column {column}"
    symbol_table["errors"].append({
        "type": "undeclared_identifier",
        "message": error_message,
        "identifier": identifier_name,
        "line": line,
        "column": column
    })


# === helper functions ===
# No helper functions needed for this simple validation logic

# === OOP compatibility layer ===
# Not needed - this is a helper function node, not a framework entry point
