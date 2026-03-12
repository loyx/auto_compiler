# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "assignment" 等)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值 (identifier 节点存储变量名)
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
#   "errors": list                 # 错误列表 [{type, message, line, column}]
# }


# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理赋值语句节点。
    
    检查目标变量是否已声明，若未声明则记录错误。
    递归遍历赋值表达式子节点。
    
    Args:
        node: assignment 类型的 AST 节点
        symbol_table: 符号表（原地修改）
    """
    # 确保 errors 列表已初始化
    if symbol_table.get("errors") is None:
        symbol_table["errors"] = []
    
    # 从 children[0] 提取目标变量（identifier 节点）
    identifier_node = node["children"][0]
    var_name = identifier_node["value"]
    line = identifier_node.get("line", node.get("line", 0))
    column = identifier_node.get("column", node.get("column", 0))
    
    # 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    var_info = variables.get(var_name)
    
    if var_info is None:
        # 变量未声明，记录错误
        symbol_table["errors"].append({
            "type": "semantic_error",
            "message": f"变量 '{var_name}' 未声明即使用",
            "line": line,
            "column": column
        })
    # 变量已声明则通过，无需操作
    
    # 递归处理赋值表达式子节点（children[1:]）
    for child in node["children"][1:]:
        _traverse_node(child, symbol_table)


# === helper functions ===
# No helper functions needed


# === OOP compatibility layer ===
# Not required for this function node
