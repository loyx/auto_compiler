# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_decl", etc.)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "target": str,           # 赋值目标变量名 (assignment 节点特有)
#   "name": str              # 变量名 (备选字段名)
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
    
    验证目标变量是否已声明，检查类型兼容性，递归处理赋值表达式中的子节点。
    副作用：可能添加错误信息到 symbol_table["errors"]
    """
    # 步骤 1: 提取目标变量名 (支持 "target" 或 "name" 字段)
    target_var = node.get("target") or node.get("name")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 步骤 2: 检查变量是否在符号表中已声明
    variables = symbol_table.get("variables", {})
    errors = symbol_table.setdefault("errors", [])
    
    if target_var not in variables:
        # 步骤 3: 未声明变量，添加错误
        errors.append({
            "type": "undeclared_variable",
            "message": f"Variable '{target_var}' is not declared before assignment",
            "line": line,
            "column": column
        })
        return
    
    # 步骤 4: 检查类型兼容性 (如果变量和值都有 data_type)
    var_info = variables[target_var]
    declared_type = var_info.get("data_type")
    value_node = node.get("value")
    
    if declared_type and isinstance(value_node, dict):
        value_type = value_node.get("data_type")
        if value_type and declared_type != value_type:
            errors.append({
                "type": "type_mismatch",
                "message": f"Type mismatch: assigning '{value_type}' to '{declared_type}' variable '{target_var}'",
                "line": line,
                "column": column
            })
    
    # 步骤 5: 递归处理赋值表达式中的子节点
    if isinstance(value_node, dict):
        _process_ast_node(value_node, symbol_table)
    elif isinstance(value_node, list):
        for child in value_node:
            if isinstance(child, dict):
                _process_ast_node(child, symbol_table)

# === helper functions ===
def _process_ast_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归处理 AST 节点。根据节点类型分发到相应的处理函数。
    当前仅处理 assignment 类型，其他类型可扩展。
    """
    node_type = node.get("type", "")
    
    if node_type == "assignment":
        _handle_assignment(node, symbol_table)
    # 其他节点类型可在未来扩展
    # elif node_type == "if":
    #     _handle_if(node, symbol_table)
    # elif node_type == "while":
    #     _handle_while(node, symbol_table)
    # elif node_type == "block":
    #     _handle_block(node, symbol_table)

# === OOP compatibility layer ===
# Not needed for this function node (not a framework entry point)
