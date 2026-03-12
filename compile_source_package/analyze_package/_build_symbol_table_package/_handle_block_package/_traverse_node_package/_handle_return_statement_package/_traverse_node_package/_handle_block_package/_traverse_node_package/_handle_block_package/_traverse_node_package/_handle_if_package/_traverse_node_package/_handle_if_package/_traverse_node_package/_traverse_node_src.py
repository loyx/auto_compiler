# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_if_package._handle_if_src import _handle_if
from ._handle_while_package._handle_while_src import _handle_while
from ._handle_for_package._handle_for_src import _handle_for
from ._handle_function_def_package._handle_function_def_src import _handle_function_def
from ._handle_variable_def_package._handle_variable_def_src import _handle_variable_def

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

ErrorRecord = Dict[str, Any]
# ErrorRecord possible fields:
# {
#   "type": str,
#   "message": str,
#   "line": int,
#   "column": int,
#   "node_type": str
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """递归遍历 AST 节点，根据类型分发到对应处理函数。"""
    try:
        node_type = node.get("type", "")
        
        # 分发到对应的处理函数
        if node_type == "if":
            _handle_if(node, symbol_table)
        elif node_type == "while":
            _handle_while(node, symbol_table)
        elif node_type == "for":
            _handle_for(node, symbol_table)
        elif node_type == "function_def":
            _handle_function_def(node, symbol_table)
        elif node_type == "variable_def":
            _handle_variable_def(node, symbol_table)
        elif node_type == "block":
            # 内联处理 block：遍历 children
            _traverse_children(node, symbol_table)
        elif node_type == "program":
            # program 节点：遍历顶层语句
            _traverse_children(node, symbol_table)
        elif node_type in ("break", "continue", "return"):
            # 控制流语句：无需特殊处理，由上层逻辑处理
            pass
        elif node_type in ("binary_op", "unary_op", "call"):
            # 表达式节点：遍历子表达式
            _traverse_children(node, symbol_table)
        elif node_type in ("literal", "identifier"):
            # 字面量和标识符：无需遍历
            pass
        else:
            # 未知节点类型：记录警告并静默跳过
            _record_unknown_node_error(node, symbol_table)
            # 仍遍历 children（如果存在）
            _traverse_children(node, symbol_table)
    except Exception as e:
        # 捕获意外异常，记录错误
        _record_traversal_error(node, symbol_table, str(e))


# === helper functions ===
def _traverse_children(node: AST, symbol_table: SymbolTable) -> None:
    """遍历节点的所有 children。"""
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)


def _record_unknown_node_error(node: AST, symbol_table: SymbolTable) -> None:
    """记录未知节点类型错误。"""
    error: ErrorRecord = {
        "type": "unknown_node_type",
        "message": f"Unknown node type encountered: {node.get('type', 'N/A')}",
        "line": node.get("line"),
        "column": node.get("column"),
        "node_type": node.get("type")
    }
    symbol_table.setdefault("errors", []).append(error)


def _record_traversal_error(node: AST, symbol_table: SymbolTable, error_msg: str) -> None:
    """记录遍历过程中的意外异常。"""
    error: ErrorRecord = {
        "type": "traversal_error",
        "message": error_msg,
        "line": node.get("line"),
        "column": node.get("column"),
        "node_type": node.get("type")
    }
    symbol_table.setdefault("errors", []).append(error)

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function node
