# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node
from ._infer_expression_type_package._infer_expression_type_src import _infer_expression_type

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "variable_declaration")
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "name": str,             # 变量名
#   "variable_type": str,    # 声明的类型 ("int" 或 "char")
#   "initial_value": Any     # 初始值（可选）
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
def _handle_variable_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """Handle variable_declaration AST nodes and update symbol table."""
    # 1. Extract variable information from node
    var_name = node.get("name")
    var_type = node.get("variable_type") or node.get("data_type")
    initial_value = node.get("initial_value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 2. Validate variable type
    if var_type not in ("int", "char"):
        symbol_table.setdefault("errors", []).append(
            f"Invalid variable type '{var_type}' for '{var_name}' at line {line}"
        )
        return
    
    # 3. Get current scope level
    current_scope = symbol_table.get("current_scope", 0)
    
    # 4. Check for duplicate declarations in current or outer scopes
    variables = symbol_table.setdefault("variables", {})
    if var_name in variables:
        existing = variables[var_name]
        existing_scope = existing.get("scope_level", 0)
        # 根据语言规范：内层作用域可以遮蔽外层同名变量
        # 只有当同名变量在同一作用域层级时才报重复声明错误
        if existing_scope == current_scope:
            symbol_table.setdefault("errors", []).append(
                f"Variable '{var_name}' already declared at line {existing.get('line', '?')}"
            )
            return
    
    # 5. Register variable in symbol table
    variables[var_name] = {
        "data_type": var_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }
    
    # 6. Process initial value if present
    if initial_value is not None:
        # 6.1 Traverse initial value expression
        _traverse_node(initial_value, symbol_table)
        
        # 6.2 Infer type of initial value expression
        inferred_type = _infer_expression_type(initial_value, symbol_table)
        
        # 6.3 Check type matching
        if inferred_type != "unknown" and inferred_type != var_type:
            symbol_table.setdefault("errors", []).append(
                f"Type mismatch in variable declaration: expected {var_type} but got {inferred_type} at line {line}"
            )

# === helper functions ===
# No helper functions needed - logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed - this is a helper function node, not a framework entry point
