# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }


# === main function ===
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点。
    
    从 AST 节点提取变量信息，注册到符号表或记录重复声明错误。
    直接修改 symbol_table，不返回任何值。
    """
    # 确保 variables 和 errors 字典存在
    symbol_table.setdefault('variables', {})
    symbol_table.setdefault('errors', [])
    
    # 从 node 提取变量信息
    var_name = node.get('value')
    data_type = node.get('data_type', 'int')
    line = node.get('line', 0)
    column = node.get('column', 0)
    
    # 检查变量是否已声明
    if var_name in symbol_table['variables']:
        # 记录重复声明错误
        error = {
            "message": f"Duplicate variable declaration: {var_name}",
            "line": line,
            "column": column,
            "node_type": "var_decl",
            "severity": "error"
        }
        symbol_table['errors'].append(error)
    else:
        # 注册新变量
        symbol_table['variables'][var_name] = {
            "data_type": data_type,
            "is_declared": True,
            "line": line,
            "column": column,
            "scope_level": symbol_table.get('current_scope', 0)
        }


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node
