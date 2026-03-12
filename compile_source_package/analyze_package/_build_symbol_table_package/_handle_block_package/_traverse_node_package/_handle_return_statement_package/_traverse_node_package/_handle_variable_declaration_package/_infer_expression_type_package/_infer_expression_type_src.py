# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed - recursive calls are self-contained

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "literal", "identifier", "binary_expression")
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "name": str,             # 变量名
#   "operator": str,         # 运算符
#   "left": AST,             # 左操作数
#   "right": AST             # 右操作数
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
def _infer_expression_type(node: AST, symbol_table: SymbolTable) -> str:
    """
    推断 AST 表达式的类型（"int"、"char"或"unknown"）。
    
    根据节点类型递归推断：
    - literal: 根据 value 的实际类型判断
    - identifier: 从符号表查找变量类型
    - binary_expression: 递归推断左右操作数，根据运算符确定结果类型
    - 其他：尝试从 data_type 字段获取或返回 unknown
    """
    if not node:
        return "unknown"
    
    node_type = node.get("type", "")
    
    # 处理 literal 类型
    if node_type == "literal":
        value = node.get("value")
        if isinstance(value, bool):
            # 布尔值返回 unknown
            return "unknown"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, str):
            if len(value) == 1:
                return "char"
            else:
                # 字符串视为 char 数组
                return "char"
        else:
            return "unknown"
    
    # 处理 identifier 类型
    elif node_type == "identifier":
        var_name = node.get("name", "")
        variables = symbol_table.get("variables", {})
        if var_name in variables:
            var_info = variables[var_name]
            return var_info.get("data_type", "unknown")
        else:
            return "unknown"
    
    # 处理 binary_expression 类型
    elif node_type == "binary_expression":
        left_node = node.get("left")
        right_node = node.get("right")
        operator = node.get("operator", "")
        
        # 递归推断左右操作数类型
        left_type = _infer_expression_type(left_node, symbol_table)
        right_type = _infer_expression_type(right_node, symbol_table)
        
        # 算术运算符: +, -, *, /
        if operator in ["+", "-", "*", "/"]:
            # 如果两边都是 int，返回 int
            if left_type == "int" and right_type == "int":
                return "int"
            # 如果涉及 char，char 提升为 int
            elif left_type == "char" or right_type == "char":
                return "int"
            else:
                return "unknown"
        
        # 比较运算符: ==, !=, <, >, <=, >=
        elif operator in ["==", "!=", "<", ">", "<=", ">="]:
            # 布尔结果用 int 表示
            return "int"
        
        else:
            return "unknown"
    
    # 处理其他类型节点
    else:
        # 尝试从 data_type 字段获取
        data_type = node.get("data_type")
        if data_type in ["int", "char"]:
            return data_type
        else:
            return "unknown"


# === helper functions ===
# No helper functions needed - all logic is in main function

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function, not a framework entry point
