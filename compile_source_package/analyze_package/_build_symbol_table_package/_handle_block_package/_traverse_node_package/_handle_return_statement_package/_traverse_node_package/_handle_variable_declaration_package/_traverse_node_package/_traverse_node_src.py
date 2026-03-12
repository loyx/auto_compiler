# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "variable_declaration", "binary_expression", "literal", "identifier")
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "name": str,             # 变量名
#   "variable_type": str,    # 声明的类型 ("int" 或 "char")
#   "initial_value": Any,    # 初始值（可选）
#   "operator": str,         # 运算符 (如 "+", "-", "*", "/")
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
def _traverse_node(node: AST, symbol_table: SymbolTable) -> Any:
    """递归遍历 AST 节点并计算表达式值。"""
    if node is None:
        return None
    
    node_type = node.get("type")
    
    if node_type == "literal":
        return node.get("value")
    
    elif node_type == "identifier":
        var_name = node.get("name")
        variables = symbol_table.get("variables", {})
        
        if var_name not in variables:
            line = node.get("line", "unknown")
            errors = symbol_table.setdefault("errors", [])
            errors.append(f"Undefined variable '{var_name}' at line {line}")
            return None
        
        var_info = variables[var_name]
        return var_info.get("value")
    
    elif node_type == "binary_expression":
        left_value = _traverse_node(node.get("left"), symbol_table)
        right_value = _traverse_node(node.get("right"), symbol_table)
        
        if left_value is None or right_value is None:
            return None
        
        operator = node.get("operator")
        
        try:
            if operator == "+":
                return left_value + right_value
            elif operator == "-":
                return left_value - right_value
            elif operator == "*":
                return left_value * right_value
            elif operator == "/":
                if right_value == 0:
                    line = node.get("line", "unknown")
                    errors = symbol_table.setdefault("errors", [])
                    errors.append(f"Division by zero at line {line}")
                    return None
                return left_value / right_value
            else:
                return None
        except Exception:
            return None
    
    else:
        return None

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function
