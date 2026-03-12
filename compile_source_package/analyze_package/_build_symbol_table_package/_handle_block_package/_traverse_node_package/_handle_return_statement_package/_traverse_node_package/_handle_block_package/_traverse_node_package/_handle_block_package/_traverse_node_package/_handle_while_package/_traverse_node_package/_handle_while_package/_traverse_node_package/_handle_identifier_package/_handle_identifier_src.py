# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub-functions needed for this simple validation logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "identifier", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (对于 identifier 节点，值为标识符名称字符串)
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
#   "errors": list                 # 错误列表 [{"message": str, "line": int, "column": int}]
# }

# === main function ===
def _handle_identifier(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理标识符节点，验证标识符是否已声明。
    
    如果标识符未在任何作用域中声明，记录错误到 symbol_table['errors']。
    如果标识符已声明，无需额外操作。
    """
    identifier_name = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 检查标识符是否在符号表的 variables 中
    if not _is_identifier_declared(identifier_name, symbol_table):
        # 记录错误
        error_message = f"标识符未声明：'{identifier_name}'"
        _record_error(symbol_table, error_message, line, column)

# === helper functions ===
def _is_identifier_declared(identifier_name: str, symbol_table: SymbolTable) -> bool:
    """
    检查标识符是否在符号表中已声明。
    
    在 symbol_table['variables'] 中查找标识符名称。
    """
    variables = symbol_table.get("variables", {})
    return identifier_name in variables

def _record_error(symbol_table: SymbolTable, message: str, line: int, column: int) -> None:
    """
    记录错误到符号表的 errors 列表中。
    
    如果 errors 列表不存在，则创建它。
    """
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    error_entry = {
        "message": message,
        "line": line,
        "column": column
    }
    symbol_table["errors"].append(error_entry)

# === OOP compatibility layer ===
# Not needed: This is a helper function node, not a framework entry point