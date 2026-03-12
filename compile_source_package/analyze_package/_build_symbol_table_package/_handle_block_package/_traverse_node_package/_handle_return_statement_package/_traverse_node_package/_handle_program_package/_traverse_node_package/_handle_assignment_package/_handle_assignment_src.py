# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "assignment", "literal", "binary_op" 等)
#   "target": str,           # assignment 节点的目标变量名
#   "expression": AST,       # assignment 节点的右侧表达式
#   "value": Any,            # 字面量节点的值
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
#   "errors": list                 # 错误列表 [{"message", "line", "column", "type"}]
# }


# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 assignment 类型节点。验证被赋值的变量是否已声明，检查类型兼容性。
    
    副作用：
    - 读取 symbol_table["variables"] 检查变量声明
    - 写入 symbol_table["errors"] 记录错误
    - 调用 _traverse_node 递归处理 expression 子节点（可能进一步修改 symbol_table）
    """
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 提取 assignment 节点信息
    target_var = node.get("target")
    expression = node.get("expression")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 检查变量是否已声明
    variables = symbol_table.get("variables", {})
    var_info = variables.get(target_var)
    
    if var_info is None:
        # 变量未声明
        symbol_table["errors"].append({
            "message": f"Assignment to undeclared variable '{target_var}'",
            "line": line,
            "column": column,
            "type": "undefined_variable"
        })
        return
    
    # 变量已声明，获取其类型
    declared_type = var_info["data_type"]
    
    # 递归处理 expression 节点
    if expression is not None:
        _traverse_node(expression, symbol_table)
        
        # 获取 expression 的类型
        expr_type = _get_expression_type(expression)
        
        # 检查类型兼容性
        if expr_type is not None and expr_type != declared_type:
            symbol_table["errors"].append({
                "message": f"Type mismatch: expected '{declared_type}' but got '{expr_type}'",
                "line": line,
                "column": column,
                "type": "type_mismatch"
            })


# === helper functions ===
def _get_expression_type(expression: AST) -> str:
    """
    从表达式节点中提取类型信息。
    
    输入：expression AST 节点
    处理：尝试从 data_type 字段或 type 字段推断类型
    返回："int"、"char" 或 None（无法推断）
    """
    if expression is None:
        return None
    
    # 优先使用 data_type 字段
    if "data_type" in expression:
        return expression["data_type"]
    
    # 尝试从 type 字段推断
    node_type = expression.get("type", "")
    if "int" in node_type:
        return "int"
    if "char" in node_type:
        return "char"
    
    return None


# === OOP compatibility layer ===
# Not required for this function node (pure helper function)
