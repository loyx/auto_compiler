# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# _traverse_node is the dispatcher located in parent package
from .. import _traverse_node

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
    处理 if 节点：遍历条件表达式和分支块。
    
    处理逻辑：
    1. 从 node["children"][0] 提取 condition 并遍历
    2. 从 node["children"][1] 提取 then_block 并遍历
    3. 如果 len(node["children"]) == 3，提取 else_block 并遍历
    
    副作用：通过 _traverse_node 递归遍历子节点，可能修改 symbol_table
    """
    children = node.get("children", [])
    
    # 至少需要 condition 和 then_block
    if len(children) < 2:
        error_msg = f"if 节点缺少必要的子节点，期望至少 2 个，实际 {len(children)} 个"
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append({
            "message": error_msg,
            "line": node.get("line", -1),
            "column": node.get("column", -1)
        })
        return
    
    # 遍历 condition (children[0])
    condition = children[0]
    _traverse_node(condition, symbol_table)
    
    # 遍历 then_block (children[1])
    then_block = children[1]
    _traverse_node(then_block, symbol_table)
    
    # 如果存在 else_block (children[2])，遍历它
    if len(children) == 3:
        else_block = children[2]
        _traverse_node(else_block, symbol_table)


# === helper functions ===
# No helper functions needed for this simple traversal logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a statement handler function
