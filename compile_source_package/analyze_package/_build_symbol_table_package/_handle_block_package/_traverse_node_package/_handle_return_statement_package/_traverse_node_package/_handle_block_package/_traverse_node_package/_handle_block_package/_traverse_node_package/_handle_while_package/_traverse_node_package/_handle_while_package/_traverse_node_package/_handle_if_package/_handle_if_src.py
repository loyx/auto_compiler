# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_src import _traverse_node

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
def _handle_if(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 if 条件语句节点。
    
    验证条件表达式类型为 'int'，遍历条件、then 分支和可选的 else 分支。
    类型错误记录到 symbol_table['errors']，不抛出异常。
    """
    line = node.get("line", 0)
    children = node.get("children", [])
    
    # 验证至少有条件 + then 分支
    if len(children) < 2:
        if len(children) < 1:
            symbol_table["errors"].append(
                f"Semantic error at line {line}: if statement missing condition expression"
            )
            return
        else:
            symbol_table["errors"].append(
                f"Semantic error at line {line}: if statement missing 'then' branch"
            )
            return
    
    condition_node = children[0]
    then_node = children[1]
    
    # 检查条件表达式类型
    condition_type = condition_node.get("data_type")
    if condition_type != "int":
        symbol_table["errors"].append(
            f"Type error at line {line}: condition expression must be of type 'int', got '{condition_type}'"
        )
    
    # 遍历条件表达式
    _traverse_node(condition_node, symbol_table)
    
    # 遍历 then 分支
    _traverse_node(then_node, symbol_table)
    
    # 如果存在 else 分支，遍历 else 分支
    if len(children) >= 3:
        else_node = children[2]
        _traverse_node(else_node, symbol_table)


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
