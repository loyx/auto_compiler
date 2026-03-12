# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===

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
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理赋值语句节点。
    验证目标变量是否已声明，并检查右侧表达式类型与变量声明类型是否兼容。
    错误记录到 symbol_table['errors']，不抛出异常。
    """
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 从 node["children"][0] 获取目标变量标识符节点
    target_node = node["children"][0]
    # 从 node["children"][1] 获取右侧表达式节点
    expr_node = node["children"][1]
    
    # 获取变量名
    var_name = target_node.get("value")
    var_line = target_node.get("line", node.get("line", 0))
    var_column = target_node.get("column", node.get("column", 0))
    
    # 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    
    if var_name not in variables:
        # 变量未声明，记录错误
        error_msg = f"变量未声明: '{var_name}' at line {var_line}, column {var_column}"
        symbol_table["errors"].append(error_msg)
        return
    
    # 变量已声明，获取声明的类型
    var_info = variables[var_name]
    declared_type = var_info.get("data_type")
    
    # 获取右侧表达式的类型
    expr_type = expr_node.get("data_type")
    
    # 如果表达式类型未知，尝试从 value 推断
    if expr_type is None:
        expr_value = expr_node.get("value")
        if isinstance(expr_value, int):
            expr_type = "int"
        elif isinstance(expr_value, str) and len(expr_value) == 1:
            expr_type = "char"
    
    # 检查类型兼容性
    if declared_type is not None and expr_type is not None:
        if declared_type != expr_type:
            # 类型不兼容，记录错误
            error_msg = f"类型不匹配: 变量 '{var_name}' 期望类型 '{declared_type}', 实际类型 '{expr_type}' at line {var_line}, column {var_column}"
            symbol_table["errors"].append(error_msg)

# === helper functions ===

# === OOP compatibility layer ===
