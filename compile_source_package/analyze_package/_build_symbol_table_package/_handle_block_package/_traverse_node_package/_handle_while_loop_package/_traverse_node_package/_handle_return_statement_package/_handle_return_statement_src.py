# === std / third-party imports ===
from typing import Any, Dict

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "value": AST,            # 返回值表达式（可选）
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _handle_return_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 return_statement 节点。
    
    从 node 中提取 "value" 字段，如果 value 不为 None，
    则递归调用 _traverse_node 遍历 value 节点。
    """
    # 延迟导入以避免循环导入
    from projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src import _traverse_node
    
    value = node.get("value")
    if value is not None:
        _traverse_node(value, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
