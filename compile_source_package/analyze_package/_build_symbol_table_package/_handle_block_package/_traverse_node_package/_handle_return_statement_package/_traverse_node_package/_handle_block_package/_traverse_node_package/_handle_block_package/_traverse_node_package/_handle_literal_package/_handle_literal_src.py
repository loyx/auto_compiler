# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple validation logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "literal", etc.)
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
def _handle_literal(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理字面量节点，验证类型与值的兼容性。
    
    处理逻辑：
    1. 从 node["data_type"] 提取类型信息（应为 "int" 或 "char"）
    2. 从 node["value"] 提取字面量值
    3. 验证类型与值的兼容性：
       - 若 data_type="int"，value 应为整数
       - 若 data_type="char"，value 应为单字符字符串
       - 若不兼容：记录类型错误到 symbol_table["errors"]
    
    所有错误记录到 symbol_table["errors"]，不抛出异常。
    """
    data_type = node.get("data_type", "")
    value = node.get("value")
    line = node.get("line", -1)
    column = node.get("column", -1)
    
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 验证类型兼容性
    if data_type == "int":
        if not isinstance(value, int):
            error = {
                "type": "error",
                "message": f"Type mismatch: expected {data_type} but got {type(value).__name__}",
                "line": line,
                "column": column
            }
            symbol_table["errors"].append(error)
    
    elif data_type == "char":
        if not isinstance(value, str) or len(value) != 1:
            actual_type = type(value).__name__
            if isinstance(value, str):
                actual_type = f"str (length={len(value)})"
            error = {
                "type": "error",
                "message": f"Type mismatch: expected {data_type} but got {actual_type}",
                "line": line,
                "column": column
            }
            symbol_table["errors"].append(error)
    
    # 其他 data_type 不做处理（可能是扩展类型或未知类型）

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function