# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._get_expression_type_package._get_expression_type_src import _get_expression_type

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
    处理赋值语句节点，验证变量已声明且类型严格匹配。
    
    处理逻辑：
    1. 从 node["children"] 中提取左侧变量名和右侧表达式
    2. 检查变量是否在 symbol_table["variables"] 中已声明
    3. 如果未声明，记录"未声明变量"错误
    4. 如果已声明，调用子函数计算右侧表达式的类型
    5. 检查右侧表达式类型与变量声明类型是否匹配
    6. 如果类型不匹配，记录"类型不匹配"错误
    """
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 获取节点基本信息
    line = node.get("line", 0)
    column = node.get("column", 0)
    children = node.get("children", [])
    
    # 检查 children 是否至少有两个元素
    if len(children) < 2:
        symbol_table["errors"].append({
            "message": "赋值语句缺少必要字段",
            "line": line,
            "column": column,
            "error_type": "INVALID_ASSIGNMENT"
        })
        return
    
    # 提取左侧变量节点
    left_node = children[0]
    
    # 检查左侧节点是否为 identifier 类型
    if left_node.get("type") != "identifier":
        symbol_table["errors"].append({
            "message": "赋值语句左侧必须是标识符",
            "line": left_node.get("line", line),
            "column": left_node.get("column", column),
            "error_type": "INVALID_ASSIGNMENT"
        })
        return
    
    # 提取变量名
    var_name = left_node.get("value")
    if var_name is None:
        symbol_table["errors"].append({
            "message": "无法提取变量名",
            "line": left_node.get("line", line),
            "column": left_node.get("column", column),
            "error_type": "INVALID_ASSIGNMENT"
        })
        return
    
    # 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    if var_name not in variables or not variables[var_name].get("is_declared", False):
        symbol_table["errors"].append({
            "message": f"变量 '{var_name}' 未声明",
            "line": line,
            "column": column,
            "error_type": "UNDECLARED_VAR"
        })
        return
    
    # 获取变量声明的类型
    declared_type = variables[var_name].get("data_type")
    
    # 提取右侧表达式节点并获取其类型
    right_node = children[1]
    right_type = _get_expression_type(right_node, symbol_table)
    
    # 如果右侧类型无法确定，跳过类型检查（错误已在子函数中记录）
    if right_type is None:
        return
    
    # 检查类型是否严格匹配
    if declared_type != right_type:
        symbol_table["errors"].append({
            "message": f"类型不匹配：变量 '{var_name}' 类型为 '{declared_type}'，但赋值为 '{right_type}' 类型",
            "line": line,
            "column": column,
            "error_type": "TYPE_MISMATCH"
        })

# === helper functions ===
# No helper functions in this file

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function
