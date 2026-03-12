# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._handle_expression_package._handle_expression_src import _handle_expression

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
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
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表
# }

# === main function ===
def _traverse_node(node: AST, symbol_table: SymbolTable) -> None:
    """
    递归遍历 AST 节点并分发到对应的处理逻辑。
    
    输入：任意 AST 节点和符号表
    处理：根据 node type 调用相应的处理逻辑
    副作用：修改 symbol_table（添加错误、更新作用域等）
    异常：无
    """
    # 确保 errors 列表存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    node_type = node.get("type", "")
    
    # 特殊节点类型处理
    if node_type == "expression":
        # 交给 _handle_expression 完整处理（包括子节点遍历）
        _handle_expression(node, symbol_table)
    
    elif node_type == "block":
        # 进入新作用域
        symbol_table["current_scope"] = symbol_table.get("current_scope", 0) + 1
        symbol_table["scope_stack"].append(symbol_table["current_scope"])
        
        # 遍历子节点
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)
        
        # 离开作用域
        symbol_table["scope_stack"].pop()
        symbol_table["current_scope"] -= 1
    
    elif node_type == "identifier":
        # 检查变量是否已声明
        var_name = node.get("value")
        if var_name and var_name not in symbol_table.get("variables", {}):
            error = {
                "type": "UNDEFINED_VARIABLE",
                "message": f"Variable '{var_name}' is not defined",
                "line": node.get("line", 0),
                "column": node.get("column", 0),
                "scope": symbol_table.get("current_scope", 0)
            }
            symbol_table["errors"].append(error)
        
        # 继续遍历子节点
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)
    
    elif node_type == "function_call":
        # 检查函数是否已声明
        func_name = node.get("value")
        if func_name and func_name not in symbol_table.get("functions", {}):
            error = {
                "type": "UNDEFINED_FUNCTION",
                "message": f"Function '{func_name}' is not defined",
                "line": node.get("line", 0),
                "column": node.get("column", 0),
                "scope": symbol_table.get("current_scope", 0)
            }
            symbol_table["errors"].append(error)
        
        # 遍历子节点（参数表达式）
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)
    
    elif node_type == "function_declaration":
        # 注册函数到符号表
        func_name = node.get("value")
        if func_name:
            functions = symbol_table.setdefault("functions", {})
            if func_name in functions:
                # 重复定义
                error = {
                    "type": "DUPLICATE_FUNCTION",
                    "message": f"Function '{func_name}' is already defined",
                    "line": node.get("line", 0),
                    "column": node.get("column", 0),
                    "scope": symbol_table.get("current_scope", 0)
                }
                symbol_table["errors"].append(error)
            else:
                functions[func_name] = {
                    "return_type": node.get("data_type", "void"),
                    "params": [],  # 从子节点解析
                    "line": node.get("line", 0),
                    "column": node.get("column", 0)
                }
        
        # 遍历子节点
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)
    
    elif node_type == "assignment":
        # 处理赋值语句，左侧 identifier 可能需要检查
        # 遍历所有子节点
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)
    
    else:
        # 其他类型（如 "program" 等）：仅递归遍历子节点
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
