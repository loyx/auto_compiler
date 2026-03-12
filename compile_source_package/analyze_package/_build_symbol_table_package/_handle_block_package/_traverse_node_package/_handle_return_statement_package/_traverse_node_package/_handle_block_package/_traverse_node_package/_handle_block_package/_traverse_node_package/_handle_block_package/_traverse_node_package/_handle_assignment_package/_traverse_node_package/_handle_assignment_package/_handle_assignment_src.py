# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed - inline implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "assignment", "literal", "identifier", etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }


# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理赋值语句节点。
    
    检查变量是否已声明，验证赋值类型与变量声明类型是否兼容。
    副作用：可能在 symbol_table["errors"] 中添加错误记录。
    """
    # Step 1: Extract target variable name from children[0] (identifier node)
    if len(node.get("children", [])) < 2:
        return
    
    target_var_node = node["children"][0]
    expr_node = node["children"][1]
    
    var_name = target_var_node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    if not var_name:
        return
    
    # Step 2: Check if variable is declared
    variables = symbol_table.get("variables", {})
    
    if var_name not in variables:
        # Variable not declared
        symbol_table["errors"].append({
            "message": f"Undefined variable: {var_name}",
            "line": line,
            "column": column,
            "severity": "error"
        })
        return
    
    var_info = variables[var_name]
    
    if not var_info.get("is_declared", False):
        # Variable defined but not formally declared
        symbol_table["errors"].append({
            "message": f"Undefined variable: {var_name}",
            "line": line,
            "column": column,
            "severity": "error"
        })
        return
    
    # Step 3: Type compatibility check
    expected_type = var_info.get("data_type", "int")
    actual_type = _infer_expression_type(expr_node, symbol_table)
    
    if expected_type != actual_type:
        symbol_table["errors"].append({
            "message": f"Type mismatch: expected {expected_type}, got {actual_type}",
            "line": line,
            "column": column,
            "severity": "error"
        })


# === helper functions ===
def _infer_expression_type(expr_node: AST, symbol_table: SymbolTable) -> str:
    """
    推断表达式的类型。
    
    通过递归遍历表达式节点，从叶子节点获取类型信息。
    """
    if not expr_node:
        return "int"
    
    node_type = expr_node.get("type", "")
    
    if node_type == "literal":
        return expr_node.get("data_type", "int")
    
    elif node_type == "identifier":
        var_name = expr_node.get("value")
        variables = symbol_table.get("variables", {})
        if var_name in variables:
            return variables[var_name].get("data_type", "int")
        return "int"
    
    elif node_type in ("binary_op", "unary_op"):
        # Recursively check first operand's type
        for child in expr_node.get("children", []):
            return _infer_expression_type(child, symbol_table)
        return "int"
    
    elif node_type == "function_call":
        func_name = expr_node.get("value")
        functions = symbol_table.get("functions", {})
        if func_name in functions:
            return functions[func_name].get("return_type", "int")
        return "int"
    
    # Default fallback
    return "int"


# === OOP compatibility layer ===
# Not needed for this function node
