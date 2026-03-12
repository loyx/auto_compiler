# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this module

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

Error = Dict[str, Any]
# Error possible fields:
# {
#   "type": str,               # 错误类型 ("error")
#   "message": str,            # 错误描述信息
#   "line": int,               # 错误发生行号
#   "column": int              # 错误发生列号
# }

# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理赋值语句节点。检查变量是否已声明，验证类型兼容性。
    """
    # 检查 value 字段是否存在
    if "value" not in node:
        _record_error(symbol_table, "Missing value field in assignment node",
                      node.get("line", -1), node.get("column", -1))
        return
    
    var_name = node["value"]
    line = node.get("line", -1)
    column = node.get("column", -1)
    
    # 检查变量是否已声明
    if var_name not in symbol_table.get("variables", {}):
        _record_error(symbol_table, f"Assignment to undeclared variable: {var_name}", line, column)
        return
    
    # 变量已声明，检查类型兼容性
    var_info = symbol_table["variables"][var_name]
    declared_type = var_info.get("data_type")
    assigned_type = node.get("data_type")
    
    if declared_type and assigned_type and not _is_type_compatible(declared_type, assigned_type):
        _record_error(symbol_table, f"Type mismatch in assignment: expected {declared_type}, got {assigned_type}", line, column)
    
    # 处理右侧表达式（如果存在 children）
    children = node.get("children", [])
    for child in children:
        if isinstance(child, dict) and child.get("type") != "literal":
            _process_expression(child, symbol_table)

# === helper functions ===
def _record_error(symbol_table: SymbolTable, message: str, line: int, column: int) -> None:
    """记录错误到符号表的 errors 列表中。"""
    error: Error = {
        "type": "error",
        "message": message,
        "line": line,
        "column": column
    }
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    symbol_table["errors"].append(error)

def _is_type_compatible(declared_type: str, assigned_type: str) -> bool:
    """检查赋值类型是否与声明类型兼容。"""
    # 当前只支持 "int" 和 "char" 两种类型
    if declared_type == assigned_type:
        return True
    # 未来可扩展类型兼容性规则（如 int 可接受字面量数字等）
    return False

def _process_expression(node: AST, symbol_table: SymbolTable) -> None:
    """处理表达式节点（递归遍历）。"""
    if not isinstance(node, dict):
        return
    
    node_type = node.get("type", "")
    
    # 处理变量引用
    if node_type == "identifier":
        var_name = node.get("value")
        if var_name and var_name not in symbol_table.get("variables", {}):
            _record_error(symbol_table, f"Use of undeclared variable: {var_name}",
                          node.get("line", -1), node.get("column", -1))
    
    # 递归处理子节点
    for child in node.get("children", []):
        if isinstance(child, dict):
            _process_expression(child, symbol_table)

# === OOP compatibility layer ===
# Not needed for this helper function module
