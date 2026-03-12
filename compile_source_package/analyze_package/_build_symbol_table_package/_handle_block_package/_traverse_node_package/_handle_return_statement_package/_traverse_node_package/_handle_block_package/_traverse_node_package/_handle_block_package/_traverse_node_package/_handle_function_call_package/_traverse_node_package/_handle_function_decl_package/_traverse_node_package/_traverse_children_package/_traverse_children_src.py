# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No direct child functions to import at module level
# _traverse_node is imported inside the function to avoid circular import

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
def _traverse_children(children: list, symbol_table: SymbolTable) -> None:
    """
    递归遍历 AST 子节点列表。
    
    对每个子节点调用 _traverse_node 进行递归处理。
    这是递归下降遍历算法的一部分，与 _traverse_node 形成递归协作关系。
    
    Args:
        children: AST 子节点列表，每个元素是一个 AST 节点（Dict）
        symbol_table: 符号表，在遍历过程中会被递归修改
    
    Side Effects:
        通过调用 _traverse_node 递归修改 symbol_table
    """
    # 在函数内部导入父函数，避免循环导入问题
    from ._traverse_node_src import _traverse_node
    
    # 如果 children 为空，直接返回（无副作用）
    if not children:
        return
    
    # 遍历每个子节点并递归调用 _traverse_node
    for child in children:
        _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node